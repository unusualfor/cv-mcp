# Technologies and partners

## Technologies

### Cloud platforms

- **Kubernetes** — primary orchestration platform for XRAN cloud-native execution, evaluated and operated from 2018 onward. Deep hands-on with scheduling, pod placement, resource isolation, NUMA locality, CPU pinning, hardware affinity, and Multus for telecom workloads. Internal training delivered across JMA engineering teams.
- **Docker** — first containerized BBU execution path built in 2018, including container topology, Linux namespaces, cgroups, device access, and PCIe visibility. Used as the baseline container runtime through the cloud-native XRAN program.
- **OpenStack** — used as internal validation platform for VM-based BBU testing, VM-vs-container comparison, and orchestration experiments (2018–2020). Research focus during university years on SDN controller integration, Neutron networking, and NFV performance.
- **Red Hat OpenShift (OCP)** — proposed as strategic CaaS direction for XRAN (2023). Detailed work plan authored covering manufacturing, air-gap installation, BBU workloads, networking, security, monitoring. Evaluated OCP EUS Term-2 for DoD compliance. Technical escalation on memory footprint, performance profiles, CPU management, and workload partitioning.
- **Red Hat OpenShift OKD** — evaluated as part of containerization platforms analysis alongside VMware Tanzu, Wind River WRCP, and internal Kubernetes (2021).
- **RHEL for Edge / bootc / MicroShift** — evaluated for DAS/Jazz-style deployments (2025), focusing on air-gapped upgrades, smaller footprint, and deployments without a traditional management server.
- **Wind River WRCP** — evaluated and deployed for a major APAC operator 5G scenarios (2021–2022). Kernel roadmap analysis (CentOS 7 / Yocto / Debian), BPF vs Preempt-RT constraints, SR-IOV setup, containerd configuration, and production patching.
- **VMware Tanzu** — assessed as part of the 2021 containerization platforms analysis.
- **AWS EKS / EKS-A / EKS-D** — evaluated for RAN workloads (2021–2023). Supported EKS + Multus PoC with CU-CP and CU-UP. Assessed EKS Anywhere and Snowball Edge for edge-platform and CaaS productization.
- **SUSE / Rancher / k3s / RKE** — evaluated for telco-edge Kubernetes (2021–2022). Investigated air-gapped deployment, PTP at the edge, and lifecycle management suitability.
- **Yocto** — assessed as an alternative bare-metal/immutable OS path for DAS/Jazz appliance models (2025).

### Networking

- **DPDK** — evaluated as Ethernet-based data-plane acceleration for XRAN, compared against InfiniBand/RDMA. Later revisited in VPP/fd.io and 6WIND contexts for IPSec and BBU data-plane improvements.
- **VPP / fd.io** — assessed as alternative IPSec acceleration path (2024), with concerns noted around Intel ecosystem dependency and productization evidence.
- **InfiniBand / RDMA** — full analysis and validation as low-latency data-plane option for XRAN inter-node communication (2018). Demonstrated potential but identified operational limits for production deployment.
- **SR-IOV** — used across multiple platforms (Kubernetes, WRCP, EKS, OpenShift) for NIC passthrough in BBU and CU-UP workloads. Ongoing consideration for link aggregation and system redundancy.
- **IPSec / strongSwan** — baseline IPSec implementation for XRAN/5G CU security. Benchmarked at approximately 1.6 Gbps on 10 Gbps link, motivating 6WIND acceleration work.
- **6WIND VSR / 6WINDGate** — high-performance IPSec acceleration achieving approximately 9.1 Gbps on 10 Gbps link (2021). Ongoing integration for the current major release on RHEL/OCP/AMD EPYC/Mellanox platforms.
- **Linux bridge** — assessed for F1-U traffic with explicit documentation of software forwarding overhead, lack of hardware acceleration, and throughput plateau risks (2025).
- **LACP / link aggregation** — system redundancy and capacity analysis for XRAN deployments, distinguishing capacity increase from redundancy use cases.
- **Multus** — used for multi-network Kubernetes pod connectivity in XRAN and EKS PoC environments.

### Timing and synchronization

- **PTP (IEEE 1588)** — deep hands-on with G.8275.1 and G.8275.2 profiles, Grandmaster and Boundary Clock configurations, T-BC/T-SC testing. Central architectural concern across XRAN, O-RAN, and DAS deployments.
- **SyncE** — evaluated as part of timing architecture alongside PTP and GNSS. Tracked availability across Fibrolan, Cisco, and NVIDIA/Mellanox platforms.
- **GNSS / GPS** — managed Cisco NCS 540 GNSS bug affecting OCXO Class C models (2021). GNSS support evaluated as architectural prerequisite for field deployment.
- **PPS in/out** — evaluated on NVIDIA/Mellanox ConnectX-6 Dx and ConnectX-7 NICs for timing synchronization use cases.

### RAN and telecom

- **XRAN / BBU** — primary workload across all JMA roles. Cloud-native execution models, containerization, performance dimensioning, and system architecture from 2018 onward.
- **5G NR** — system architecture for gNB CU-CP, CU-UP, and DU components across multiple software releases (earlier releases through SR-05).
- **4G LTE / eNB** — multi-operator eNB configurations (Cisco Luminet lab), CBRS integration, and coexistence with 5G in XRAN deployments.
- **O-RAN** — M-Plane enablement (WG4), standards tracking (WG11), plugfest participation, third-party O-RU integration, and O-RAN POI architecture for DAS. Delegate at four O-RAN Alliance F2F meetings (2024–2026).
- **3GPP** — standards strategy and monitoring, delegate at RAN Plenary #111 (Fukuoka, 2026). 6G study tracking through nGRG workshops.
- **eCPRI / CPRI** — fronthaul protocols for O-RAN and DAS architectures, including RF-to-eCPRI POI and Cat-A/Cat-B variants.
- **DAS** — DAS 3.0/NG2/Jazz system architecture from 2025, covering RU variants, switch integration, supervisor connectivity, vPOI PTP, and timing.
- **NETCONF / YANG** — concrete requirements definition for switch management, O-RU M-Plane integration, and OpenConfig model adoption across Fibrolan, Cisco, and Ciena.
- **CBRS** — shared spectrum access system integration, including Cisco CBRS project support and patent on multi-operator virtual base station in shared spectrum.

### Hardware

- **x86 / AMD EPYC** — primary server platforms for XRAN and DAS deployments. BIOS tuning, CPU pinning, NUMA configuration, and performance profiling.
- **NVIDIA/Mellanox ConnectX-4 Lx / 5 / 6 Dx / 7** — multi-year NIC strategy from 2018. PTP, PPS in/out, SyncE, SR-IOV, firmware management, and O-RAN fronthaul readiness evaluation across generations.
- **Intel E810** — assessed and kept out of near-term production options due to maturity concerns (2021).
- **Intel ACC100** — evaluated as hardware accelerator comparison point for BBU performance.
- **Cisco NCS 540** — primary timing switch family for XRAN and O-RAN deployments. PTP configuration expertise for G.8275.1 and G.8275.2, GNSS bug management, firmware updates, and NETCONF/YANG management.
- **Cisco ASR 920** — early PTP timing switch, used for G.8275.2 Boundary Clock and IPSec scenarios (2019). Superseded by NCS 540.
- **Advantech** — server platform for DAS 3.0/Jazz, including RHEL9/RHCOS memory footprint evaluation and reduced-footprint OCP assessment.
- **Xilinx / AMD-Xilinx RFSoC / Versal** — Massive MIMO O-RU platform evaluation, M-Plane profile assessment, and later connection to DAS/Jazz O-RAN POI and Distributed Massive MIMO architecture.

### AI/ML

- **GitHub Copilot** — structured the DAS 3.0 AI pilot (2026) with governance, KPIs, monthly checkpoints, and budget justification for engineering productivity evaluation.

### Observability

- **Prometheus** — used for monitoring and benchmarking containerized XRAN components (2019–2020), correlating system-level metrics with BBU performance for data-driven architectural decisions.

## Partners

### Platform vendors

- **Red Hat** — strategic platform partner for OCP, RHEL, bootc, and MicroShift. Technical escalation on platform issues, Red Hat Summit attendance, and evaluation of RHEL for Edge for DAS/Jazz (2023–2026).
- **Wind River** — WRCP deployment and production support for a major APAC operator, kernel profile analysis, and containerization platform comparison (2021–2022).
- **VMware** — Tanzu evaluated as part of containerization platforms analysis (2021).
- **SUSE / Rancher** — telco-edge Kubernetes evaluation, air-gap and lifecycle management assessment, and Nephio/Linux Foundation tracking (2021–2022).

### Networking vendors

- **Cisco** — extensive hands-on with NCS 540 timing switches and PTP validation (2020–2022), ASR 920 early timing (2019), Luminet lab integration tests (2019), CBRS project support (2019), Paris lab O&M/NSO integration (2019), NSO/ESC/MANO and NETCONF/YANG NED development discussions.
- **Juniper** — IPsec/Security Gateway integration for a European operator Open RAN, debugging certificate trust chains and AutoVPN behavior (2021).
- **Fibrolan** — multi-phase timing and Sync Controller validation (2022–2023), NETCONF/YANG management workflow review, on-site Bologna sessions, PTP/SyncE/GNSS evaluation, and field-readiness approval conditioning.
- **Ciena** — interoperability evaluation reframed to align product portfolios before engineering engagement, Phase-1 test plan updates (2022).
- **6WIND** — high-performance IPSec acceleration from initial contact (2020) through benchmarking (9.1 Gbps, 2021), Cell Site Router re-evaluation (2022), and ongoing the current major release integration on RHEL/OCP/AMD EPYC (2024–2025).

### Cloud providers

- **AWS** — EKS/EKS-A/EKS-D evaluation for RAN workloads, Snowball Edge assessment, EKS + Multus PoC, and OEM agreement discussions (2021–2023).

### Silicon vendors

- **NVIDIA / Mellanox** — multi-year NIC strategy from InfiniBand/RDMA analysis (2018) through ConnectX-6 Dx evaluation (2020), PTP T-BC/T-SC testing (2021), ConnectX-5/7 assessment, firmware management, and procurement alignment. NVIDIA Omniverse Digital Twin exploration (2024).
- **Intel** — FlexRAN release material and enablement discussions, NIC assessment (x710/x810), ACC100 accelerator evaluation, and platform-level CPU/DDIO considerations (2022).
- **Xilinx / AMD-Xilinx** — Massive MIMO O-RU platform evaluation including M-Plane profile, SSH algorithm support, SFP28/FEC behavior, and GNSS availability (2021).

### Hardware vendors

- **Advantech** — server platform for DAS 3.0/Jazz, RHEL9/RHCOS footprint validation (2025–2026).
- **Dell** — server platforms for XRAN labs; resolved Dell-branded Mellanox firmware/PSID issues (2022). R750 used for NVIDIA Digital Twin exploration (2024).

### Radio and system integration vendors

- **MTI** — early O-RU/RRH M-Plane integration, NETCONF details, bootstrapping procedures, and DHCP/call-home support investigation (2020–2022).
- **Fujitsu** — O-RAN radio integration in TIM/JMA context, C/U-plane and S-Plane review, SyncE and fronthaul behavior clarification (2021–2022).
- **Mavenir** — O-RU integration analysis for TIM macro/O-RAN scenarios, identification of non-standard M-Plane parameters outside O-RAN YANG models (2022).
- **Italtel** — introductory technical engagement around Open RAN architectures, system integration, and fronthaul constraints (2019).
- **IP Infusion** — switch elements for DAS 3.0/NG2 architecture (2025).

### Operators

- **TIM** — European operator lab O-RAN plugfest preparation, timing validation, Cisco NCS 540 deployment, and Fujitsu/Mavenir O-RU integration context (2020–2022).
- **a major APAC operator** — Wind River WRCP deployment, kernel profile analysis, and XRAN production support (2021–2022).
- **Vodafone** — a European operator Open RAN Security Gateway integration with Juniper (2021); a European operator coordination.
- **Verizon** — operator RFP context (2019).

### Standards bodies and industry groups

- **O-RAN Alliance** — delegate at four F2F meetings (Athens 2024, Incheon 2024, Dallas 2025, Rome 2026). WG4 M-Plane work, WG11 change requests, nGRG 6G workshop participation, and plugfest-based interoperability.
- **3GPP** — delegate at RAN Plenary #111 (Fukuoka 2026). Standards monitoring and strategic assessment.
- **TIP (Telecom Infra Project)** — plugfest participation and external interoperability pressure.
- **AI-RAN Alliance** — technical overview and roadmap tracking (2026).
