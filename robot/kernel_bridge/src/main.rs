//! Transport only. All A/rho/B/R and persistence math stays in canonical V9.
use abr_kernel::{diagnostic_exec as dx, operators::EdgeProvenance};
use serde_json::{json, Value};
use std::io::{self, BufRead, Write};

fn field(config: &Value, stage1: &Value, request: &Value) -> Result<dx::ExperimentalField, String> {
    let vals = request["values"].as_array().ok_or("values array required")?;
    if vals.len()!=4 { return Err("exactly four node values required".into()); }
    let mut nodes=Vec::new();
    for (i,n) in stage1["abr_topology"]["nodes"].as_array().ok_or("nodes missing")?.iter().enumerate() {
        let id=n["id"].as_str().ok_or("node id missing")?;
        nodes.push(dx::NodeRecord {id:id.into(), values:vec![vals[i].as_f64()],
            measurement:dx::MeasurementSupport::Declared(config["measurement_mapping"][id].to_string())});
    }
    let edges=stage1["abr_topology"]["edges"].as_array().ok_or("edges missing")?.iter().map(|e| {
        Ok(dx::EdgeRecord {id:e["id"].as_str().ok_or("edge id")?.into(),
            source:e["from_node"].as_str().ok_or("source")?.into(),target:e["to_node"].as_str().ok_or("target")?.into(),
            provenance:dx::EdgeProvenanceRecord {class:EdgeProvenance::Coupling,support:dx::RelationSupport::Observed,
                basis:Some(format!("independently logged {} software delivery to {}.information_inbox; no physical coupling measurement asserted",e["id"],e["to_node"]))}})
    }).collect::<Result<Vec<_>,String>>()?;
    Ok(dx::ExperimentalField {field_id:config["field_id"].as_str().ok_or("field_id")?.into(),
        observation_id:request["observation_id"].as_str().ok_or("observation_id required")?.into(),
        process_step:request["process_step"].as_u64().ok_or("process_step required")?,n_components:1,
        nodes,edges,component_pairs:vec![],parameters:Some(dx::RhoParameters::General{chi_unit:"m".into()}),
        experimental_arrangement:Some("Simulated component I/O; declared design geometry and persistent instruction are not environmental measurements".into()),
        unresolved_conditions:vec!["The metre-valued component projection mixes geometry, range, wheel encoder travel and a reference. Outputs characterize the declared information field, not inter-component spatial distances.".into()]})
}

fn warnings(ws: &[dx::Warning]) -> Value { json!(ws.iter().map(|w|json!({"class":format!("{:?}",w.class),"item":w.item,"detail":w.detail,"reference":w.reference})).collect::<Vec<_>>()) }
fn bits(rows: &[Vec<f64>]) -> Value {json!(rows.iter().map(|r|r.iter().map(|v|format!("{:016x}",v.to_bits())).collect::<Vec<_>>()).collect::<Vec<_>>())}
fn spatial(x: &dx::SpatialExecution) -> Value {
    json!({"field_id":x.field_id,"observation_id":x.observation_id,"process_step":x.process_step,
        "node_ids":x.node_ids,"edge_ids":x.edge_ids,"edge_endpoints":x.edge_endpoints,
        "A":x.a.spatial,"rho":x.rho,"B":x.b.spatial,"R":x.r.spatial,
        "f64_bits":{"A":bits(&x.a.spatial),"B":bits(&x.b.spatial),"R":bits(&x.r.spatial),
            "rho":x.rho.iter().map(|v|format!("{:016x}",v.to_bits())).collect::<Vec<_>>()}})
}

fn execute(f: &dx::ExperimentalField, prior: &mut Option<dx::SpatialExecution>) -> Value {
    let result = if let Some(p)=prior.as_ref() {
        dx::execute_with_prior(f,p).map(|p| {
            let v=json!({"status":"EXECUTED","function":"diagnostic_exec::execute_with_prior","spatial":spatial(&p.current),
                "persistence":{"prior_observation_id":p.prior_observation_id,"A":p.persistence.a_persistence,
                    "rho":p.rho_persistence,"B":p.persistence.b_persistence,"R":p.persistence.r_persistence,
                    "f64_bits":{"A":bits(&p.persistence.a_persistence),"B":bits(&p.persistence.b_persistence),"R":bits(&p.persistence.r_persistence)}},
                "kernel_diagnostics":warnings(&p.warnings)});
            (p.current,v)
        })
    } else {dx::execute_spatial(f).map(|x| {let v=json!({"status":"EXECUTED","function":"diagnostic_exec::execute_spatial",
        "spatial":spatial(&x),"persistence":null,"kernel_diagnostics":warnings(&x.warnings)});(x,v)})};
    match result {
        Ok((x,mut v))=>{v["kernel_debug"]=json!(format!("{x:#?}"));*prior=Some(x);v},
        Err(e)=>json!({"status":"NOT_EXECUTED","errors":e.errors.iter().map(|e|json!({"class":format!("{:?}",e.class),"item":e.item,"detail":e.detail})).collect::<Vec<_>>(),"kernel_diagnostics":warnings(&e.warnings)})
    }
}

fn main() {
    let args:Vec<_>=std::env::args().collect();
    let config:Value=serde_json::from_slice(&std::fs::read(&args[1]).expect("config read")).expect("config parse");
    let stage1:Value=serde_json::from_slice(&std::fs::read(&args[2]).expect("Stage 1 read")).expect("Stage 1 parse");
    let mut prior=None;
    for line in io::stdin().lock().lines() {
        let response=match line.map_err(|e|e.to_string()).and_then(|s|serde_json::from_str::<Value>(&s).map_err(|e|e.to_string()))
            .and_then(|r|field(&config,&stage1,&r)) {
                Ok(f)=>execute(&f,&mut prior),Err(e)=>json!({"status":"INPUT_ERROR","detail":e})};
        println!("{}",response);io::stdout().flush().unwrap();
    }
}

#[cfg(test)] mod tests {
    use super::*;
    fn input()->dx::ExperimentalField {
        let root=std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
        let cfg:Value=serde_json::from_slice(&std::fs::read(root.join("robot/config.json")).unwrap()).unwrap();
        let st:Value=serde_json::from_slice(&std::fs::read(root.join("field/stage1_robotics_domain.json")).unwrap()).unwrap();
        field(&cfg,&st,&json!({"values":[0.12,0.8,0.0,0.1],"observation_id":"test/1","process_step":1})).unwrap()
    }
    #[test] fn exact_canonical_outputs_and_reciprocal_identity() {
        let f=input();let direct=dx::execute_spatial(&f).unwrap();let v=execute(&f,&mut None);
        assert_eq!(v["spatial"],spatial(&direct));assert_eq!(direct.edge_ids.len(),12);
        assert_eq!(direct.edge_endpoints[0],("N1".into(),"N2".into()));
        assert_eq!(direct.edge_endpoints[1],("N2".into(),"N1".into()));
    }
    #[test] fn missing_signal_never_filled() {
        let mut f=input();f.nodes[2].values[0]=None;
        let mut prior=None;let v=execute(&f,&mut prior);
        assert_eq!(v["status"],"NOT_EXECUTED");assert!(prior.is_none());assert!(v.get("spatial").is_none());
    }
    #[test] fn repeated_state_has_real_persistence_and_gap_refused() {
        let mut f=input();let mut prior=None;execute(&f,&mut prior);
        let direct_prior=prior.clone().unwrap();f.process_step=2;f.observation_id="test/2".into();
        let direct=dx::execute_with_prior(&f,&direct_prior).unwrap();let v=execute(&f,&mut prior);
        assert_eq!(v["persistence"]["R"],json!(direct.persistence.r_persistence));
        f.process_step=4;f.observation_id="test/4".into();
        assert_eq!(execute(&f,&mut prior)["status"],"NOT_EXECUTED");assert_eq!(prior.unwrap().process_step,2);
    }
}
