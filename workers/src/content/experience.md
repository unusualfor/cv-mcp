# Experience

## JMA Wireless

### Director, Software Architecture — Aug 2024 – present

Bologna metropolitan area, Italy

Defines and drives technology strategy and architecture direction across carrier, enterprise, and federal / defense market segments, with focus on research initiatives, standards engagement, and system architecture for DAS/RAN convergence.

**Key work:**

- Built a strategic standards-engagement proposal for JMA, recommending a sustainable 3GPP/O-RAN monitoring and participation model with FTE justification and working-group prioritization.
- Led DAS 3.0/Jazz architecture planning and supported development, covering RF-to-eCPRI POI and variants, O-RAN POI variants, RU/switch/supervisor integration, and PoC framing with support to multiple feasibility checkpoints, High Level Architecture design, support to Low Level Architecture definition, Feature Requirements Specification definition, integration validation (PTP/SyncE, G.8275.1, DHCP/NETCONF call-home, etc.).
- Drove advanced development inputs for BBU and platform evolution, including Distributed Massive MIMO, DPDK/VPP-based data plane, edge OS (Yocto, bootc, MicroShift, etc.).
- Escalated and structured partner technical issues affecting XRAN product releases.
- Evaluated RHEL for Edge, bootc, and MicroShift for DAS/Jazz deployments.
- Provided system architecture guidance on XRAN networking: link aggregation, Linux networking limitations, SR-IOV implications, and redundancy/capacity design guidelines.
- Drove XRAN architecture governance including release-level requirements alignment and Red Hat OpenShift PoCs.
- Advanced Red Hat/OCP and AI-platform strategy: CaaS layer assessment comparing Red Hat, Wind River, and VMware; AI for RHEL/RHOCP evaluation; AIOps and SMO-like OCP platform framing.
- Structured the GitHub Copilot AI pilot for R&D with governance, KPIs, monthly checkpoints, and management-facing material.
- Continued O-RAN/6G strategic tracking, including potential change requests, nGRG 6G workshop inputs, and O-Cloud technical strategy.
- Coordinated 2025 research/university collaboration pipeline with University di Bologna; delivered network automation teaching material and edge-computing seminars.
- Supported DAS 3.0 integration coordination covering single-fiber server/switch connectivity, PTP drift and holdover, G.8275.1 chain validation, breakout cabling, and O-RU Controller reuse.
- Supported large-venue DAS system analysis, contributing RU-to-sector mapping inputs for stadium and arena-scale deployments.
- Drove engineering partners escalation covering memory footprint gaps, reduced-footprint for private wireless/tactical scenarios, SSO/reverse proxy access, performance issues, CPU management, workload partitioning, and high memory consumption in kernel 5.x.
- Evaluated EUS Term-2 support for security needs; framed the risk that OCP footprint/performance overhead could force alternatives such as bare-metal edge nodes based on Yocto.
- Attended Red Hat Summit and recommended a closer partnership loop.
- Structured the 2025 research pipeline with candidate topics for XRAN and DAS.
- Tracked high-performance IPSec CPU-core isolation requirements for XRAN E2E security and dimensioning, including the need for dedicated isolated cores and impact on BBU sizing.
- Supported JMA visibility at CNSM 2025 through sponsorship coordination, participated in RESTART Phase 2-related evaluation, and contributed to WCNC 2025 as panelist.
- Structured external collaboration scope for 3GPP/O-RAN standards monitoring and assessment.
- Delivered "Distributed Systems Edge — Navigating the Distributed Complexity" seminar at Università di Bologna for the Programmable Networks course.
- Delivered 10 hours MSc Course + Lab about "Distributed Systems"at Università di Bologna course.

### Principal Software Architect — Feb 2023 – Aug 2024

Bologna metropolitan area, Italy

Defined mid-term and long-term product architecture direction for the XRAN portfolio, with scope expanding toward system-of-systems ownership anticipating XRAN BBU and DAS Jazz convergence.

**Key work:**

- Proposed and coordinated the XRAN Plugfest program as a structured integration feedback mechanism, with plugfest timing tied to development sprints and architecture workshops. On-site lab work in Boulder (May 2023, Jul 2023, Sep 2023, Jan 2024) supported integration validation and direct feedback from development and performance engineers.
- Coordinated multiple technical sessions with networking partners (e.g. Cisco, Fibrolan, Ciena), including on-site validation in Bologna with architecture, QA, and system stakeholders.
- Framed CaaS productization as a comparative architecture topic across AWS EKS-A, Rancher/SUSE, SpectroCloud Palette, focusing on what could be productized, supported, automated, and operated. 
- Red Hat partnership setup for PaaS evaluation of OpenShift. Authored a detailed Red Hat OpenShift work plan splitting the effort into phases: manufacturing, air-gap installation, BBU workloads, networking, security, monitoring, and documentation.
- Drove high-performance IPSec evaluation, porting to Kubernetes, and alternatives analysis (VPP/fd.io, strongSwan with DPDK fastpath), eventually leaning towards a full DPDK/VPP rework.
- Contributed to O-Cloud technical strategy and federal market platform development.
- Expanded university and research collaboration with University of Bologna and Saint Louis University.
- Prepared and delivered NetSoft 2024 ENS keynote: "Smooth sailing ahead? Navigating the Edge challenges, and preparing to correct the course."
- Proposed architectural improvements to JMA implementation of O-RAN M-Plane O-RU Controller configuration model, advocating for a template-based approach for radio configuration before call-home to improve repeatability and reduce ad-hoc per-radio handling.
- Explored potential university collaboration around NPN / 5G-in-a-box / O-RAN open-source feasibility.
- Supported NVIDIA partnership through Omniverse Digital Twin exploration, coordinating access to a Dell platform.

### Manager, 5G O&M and Cloud — Sep 2021 – Feb 2023

Bologna metropolitan area, Italy

Led a team of ten engineers through the cloud transition of the XRAN portfolio, with responsibility expanding into O-RAN management, timing architecture, vendor interoperability, and field-readiness concerns.

**Key work:**

- Defined concrete NETCONF/YANG requirements for switch management covering configuration, L2/L3 interfaces, VLANs, timing (GNSS, PTP, SyncE), QoS (DSCP, PCP), mirroring, fault management, and performance measurements. Pushed for OpenConfig YANG model adoption for multi-vendor consistency across Fibrolan, Cisco, and Ciena.
- Elevated timing architecture (PTP, SyncE, GNSS) from optional enhancement to gating prerequisite for field deployment. 
- Managed vendor interoperability directly: coordinated QA to validate switches under production-level traffic; structured interop discussions to align product portfolios before engineering engagement.
- Drove practical multi-vendor O-RU integration analysis across MTI, Fujitsu, Mavenir, and JMA O-RAN radios, exposing the gap between nominal O-RAN compliance and what was required for field operation.
- Supported Wind River WRCP production deployment for a major APAC operator, resolving containerd/SR-IOV/NIC issues; authored containerization platforms analysis comparing VMware Tanzu, Wind River WRCP, Red Hat OpenShift/OKD, and internal Kubernetes.
- Led Juniper Security Gateway integration for a European operator's Open RAN deployment, debugging certificate trust chains, AutoVPN behavior, and strongSwan configuration alignment.
- Drove high-performance IPSec benchmarking (9.1 Gbps achieved on 10 Gbps link vs 1.6 Gbps with strongSwan).
- Assessed CaaS platform landscape: AWS EKS-A/Snowball Edge, SUSE/Rancher, and NVIDIA/Mellanox NIC strategy consolidation.
- Routed networking technical training (O-RAN, PTP theory, timing troubleshooting, switch configuration) to QA and development teams.
- Contributed to JMA roadmap discussions ensuring items reflected real integration cost and sequencing for O-RAN and M-Plane enablement across Architecture, QA, RF Conformance, and Development teams.
- Supported the maturation of the O-RAN products implementation direction, clarifying that radio integration required lifecycle handling, M-Plane configuration, DHCP/call-home behavior, and repeatable configuration workflows beyond C/U-plane compliance.
- Identified non-standard O-RU partner M-Plane behavior outside official O-RAN YANG models, reinforcing that third-party O-RU integration required detailed vendor cooperation and product-level workflows.
- Supported APAC partner training course setup on WRCP, including hardware compatibility assessment and NIC requirements; captured the architectural constraint that WRCP real-time OS conflicted with the proposed shared architecture.
- Re-evaluated Cell Site Router architectures, identifying compatibility limitations between high-performance IPSec, WRCP, and XRAN requirements.
- Resolved Dell-branded Mellanox firmware issues and clarified PSID/firmware management constraints for ConnectX-6 Dx procurement.
- Drove detailed technical assessment of AWS Snowball Edge for RAN use cases, documenting concerns around Ubuntu-based VM assumptions, SR-IOV behavior, CPU pinning, NIC uncertainty, and air-gapped operator environments.
- Continued SUSE/Rancher engagement around telco-edge Kubernetes, including MWC-related discussions on k3s, SLE Micro, and Nephio/Linux Foundation ecosystem tracking.
- Engaged with Intel around FlexRAN release material, ACC100 accelerator evaluation, and NIC options (x710/x810) for XRAN backhaul, midhaul, and fronthaul needs.
- Assessed Cisco ASR 920 for operator-related fronthaul usage and halted the activity as it was superseded by the NCS 540 direction.

### System Architect — Apr 2019 – Sep 2021

Bologna, Italy

Primary technical reference for XRAN virtualization and containerization feasibility, bridging infrastructure experimentation with real BBU software behavior and performance constraints.

**Key work:**

- Continued and deepened the cloud-native XRAN program: systematic evaluation of BBU execution across bare metal, VMs, and containers, with focus on performance degradation sources (scheduler behavior, interrupt handling, PCIe access, CPU pinning).
- Formalized the architectural separation between BBU real-time critical paths and ancillary services, establishing that not all BBU-related software must share the same execution model.
- Investigated low-latency data-plane options (InfiniBand/RDMA vs Ethernet/DPDK) and their long-term architectural implications; established that data-plane choices would strongly constrain future architecture.
- Identified limitations of vanilla Kubernetes for XRAN use cases (latency, NUMA locality, hardware affinity) and documented these as architectural risks.
- Built Prometheus-based monitoring and benchmarking practices for containerized XRAN, correlating system-level metrics with BBU performance.
- Built deep Cisco NCS 540 PTP configuration expertise for G.8275.1 and G.8275.2 profiles, including Grandmaster and Boundary Clock use cases. Managed NCS 540 deployment across multiple operator lab environments.
- Started MTI O-RU M-Plane integration, translating generic O-RAN WG4 expectations into concrete NETCONF integration questions.
- Evaluated NVIDIA/Mellanox ConnectX-6 Dx NICs (PPS in/out, PCIe 4.0, crypto) and performed PTP T-BC/T-SC testing.
- Led Cisco lab integration tests in Milan (multi-operator configuration, VLAN isolation, DSCP/QoS through IPSec tunnels), Cisco CBRS project support, and Cisco Paris lab setup for O&M/NSO integration.
- Acted as bridge between European and US XRAN teams, aligning assumptions around BBU execution, virtualization constraints, and deployment expectations through combined on-site lab windows and remote collaboration.
- Consolidated containerized XRAN work into reproducible, automation-friendly setups during COVID-era constraints, shifting emphasis from experimentation to operational robustness and repeatability.
- Maintained and evolved the internal OpenStack environment as a complementary validation platform to Kubernetes, used for VM-based BBU testing, CU-CP/CU-UP execution, and orchestration experiments.
- Used Cisco ASR 920 as the first timing switch for PTP validation, configured for G.8275.2 and G.8275.1 Boundary Clock usage.
- Participated in an introductory technical engagement around Open RAN architectures, system integration roles, fronthaul constraints, and timing implications.
- Drove Cisco NSO / ESC / MANO discussions for XRAN, including NETCONF/YANG NED development and orchestration-model analysis.
- Used Cisco NCS 540 in support of European O-RAN plugfest preparation and timing validation.
- Started discussions with network partners around high-performance IPSec offload, driven by the gap between baseline strongSwan IPSec performance and throughput needed for realistic 5G traffic.
- Supported early 3PP O-RAN radio integration, reviewing C/U-plane, prioritization, S-Plane, SyncE, and fronthaul-related assumptions.
- Discovered and managed a GPS/GNSS bug affecting Cisco NCS 540 timing behavior with OCXO Class C models; drove evidence-based escalation while protecting customer-facing programs from unnecessary impact.
- Participated in Cisco NYAT / NETCONF YANG Automation Testing discussions, including evaluation of DrNED-style testing approaches.
- Engaged in early evaluation of the AMD/Xilinx O-RAN Massive MIMO O-RU platform, reviewing IOT profiles and assessing M-Plane implications for JMA integration.
- Participated in early JMA/AWS technical engagement around EKS for RAN workloads; supported a successful AWS Kubernetes + Multus PoC where EMS, gNB CU-CP, and CU-UP were orchestrated on AWS EKS containers.
- Engaged with SUSE/Rancher for telco-edge Kubernetes evaluation, investigating Rancher/k3s/RKE assumptions for air-gapped deployment, PTP handling at the edge, and operational suitability in telco environments.
- Consolidated NVIDIA/Mellanox NIC strategy: ConnectX-5 as successor to ConnectX-4 Lx, ConnectX-7 as future option for PPS in/out, and Intel E810/Edgewater as an alternative, supporting Intel in debug phases until reached maturity.

### Networking System Design Engineer — Jul 2018 – Apr 2019

Bologna, Italy

Joined JMA Wireless to explore cloud-native execution models for the XRAN baseband processing software, working under a research-mode mandate without product-delivery pressure.

**Key work:**

- Completed the first PoCs of XRAN running in Docker containers (Sep–Nov 2018), establishing the initial containerized BBU execution path including container topology, Linux namespaces, cgroups, device access, and PCIe visibility.
- Built the first Kubernetes-based experimentation environment for XRAN components.
- Conducted full InfiniBand/RDMA analysis and validation as a low-latency data-plane option for XRAN inter-node communication (Aug–Sep 2018).
- Contributed to patent on Kubernetes/container orchestration for BBU.
- Evaluated OpenStack and Kubernetes networking suitability for telecom-grade workloads, concluding that default cloud-networking assumptions were insufficient for XRAN latency and determinism requirements.
- Identified and debugged critical PCIe access issues affecting BBU execution inside containers, creating the technical foundation for later XRAN containerization and cloud-native activities.
- Presented InfiniBand findings, demonstrating RDMA potential while clarifying the operational limits of introducing a specialized fabric into XRAN deployments.

## Laboratori Guglielmo Marconi

### System and Network Engineer — Nov 2017 – Jun 2018

Bologna, Italy

Design, implementation, and monitoring of IP networks and systems for public-sector and large-scale private organizations, with support to the internal Network and Security Operations Center.

**Key work:**

- Executed a zero-downtime system and network migration of a city-wide hospital network.
- Completed full integration of a large-scale retail operation into a 24/7 live monitoring mesh.
- Managed end-to-end customer requirements through delivery, bridging the gap between academic research and industrial network engineering.

## Huawei Technologies

### Intern — Seeds for the Future Program — Mar 2017

Shenzhen, Guangdong, China

Selected as one of the top ten Italian ICT students for the Huawei Seeds for the Future program, a competitive international initiative combining telecommunications R&D immersion with cross-cultural exchange.

**Key work:**

- One-month immersion in Shenzhen providing exposure to large-scale network deployment strategies and collaboration with global engineering teams working on 2G, 3G, and 4G technologies.
- Concurrent with the Beijing Language and Culture University experience program in Chinese language and culture.

## Università di Bologna

### Cloud Solutions Designer — Nov 2014 – Oct 2017

Bologna, Italy

Research-track position concurrent with the Bachelor's and Master's programs, leading cloud computing and SDN research with focus on OpenStack–SDN controller integration.

**Key work:**

- Produced four peer-reviewed conference publications and received the IEEE Best Paper Award (ICC 2018) for work on native SDN integration within OpenStack.
- Designed and deployed cloud clusters for EU-funded cooperative research projects through the European Institute of Innovation and Technology (EIT) framework.
- Developed a performance evaluation framework for SDN controllers (Ryu, ONOS, OpenDaylight).
- Supervised graduating students on cloud computing and networking projects.
- Served as teaching assistant for the BSc "TLC Networks" course.
- Visiting scholar at UCLA (2015) as part of an international research collaboration.

---

# Patents

1. **Orchestrator and interconnection fabric mapper for a virtual wireless base station** — US12089071B2, United States. Granted. Inventors: Massimo Notargiacomo, Jeffrey Courington, Stephen Turner, Jeffrey Masters, Vishal Agrawal, Francesco Foresta. Assignee: PPC Broadband Inc.
2. **Integrated radio network with multi operator and multi signal format fronthaul capability** — US11856449B2, United States. Granted. Inventors: Massimo Notargiacomo, Gilberto Brizzi, Francesco Foresta, Alessandro Pagani, Giovanni Chiurco, Giulio Gabelli, Davide Durante, Fabrizio Marchese, Richard Wank, Michael Tierney. Assignee: PPC Broadband Inc.
3. **System and method for securely hosting multiple network operators in a shared spectrum access system on a single virtual base station environment** — US20210029549A1, United States. Published. Inventors: Massimo Notargiacomo, Todd Landry, Jeffrey Masters, Roberto Orlandini, Jeffrey Courington, Francesco Foresta, Stephen Turner, Alessandro Pagani, Domenico Di Iorio, Kurt Jacobs, Patrick Henkle, Vishal Agrawal, Sasi Eswaravaka, Paul Stath.
4. **Blockchain-based method and system for securing a network of virtual wireless base stations** — WO2021041937A1, WIPO (PCT). Published. Inventors: Jeffrey Courington, Francesco Foresta, Vishal Agrawal.

# Standards Delegate Attendance

- O-RAN Alliance F2F — Athens, Greece, Feb 2024. Delegate, JMA Wireless.
- O-RAN Alliance F2F — Incheon, South Korea, Jun 2024. Delegate, JMA Wireless.
- O-RAN Alliance F2F — Dallas, TX, USA, Nov 2025. Delegate, JMA Wireless.
- O-RAN Alliance F2F — Rome, Italy, Feb 2026. Delegate, JMA Wireless.
- 3GPP RAN Plenary 111 — Fukuoka, Japan, Mar 2026. Delegate, JMA Wireless.

# Teaching and Training

## University Lectures and Seminars

- 2022 — "Next-generation open cellular networks" — Syracuse University, guest lecture.
- 2022 — "Enabling smarter mobile solutions through SDN and NFV" — Università di Bologna, TLC projects session.
- 2023 — "Empowering smarter mobile solutions through network softwarization" — Università di Bologna, lecture / seminar.
- 2025 — "Software Defined Networking — Network Management Automation" — Università di Bologna, Principles, Models and Applications for Distributed Systems M.
- 2025 — "Advanced Distributed Systems in Kubernetes" — Università di Bologna, Principles, Models and Applications for Distributed Systems M.
- 2025 — Network automation lab — Università di Bologna. Lab material with NETCONF tooling, Python scripting, Ansible, approximately 10 hours of guest lectures.
- 2026 — "Distributed Systems Edge — Navigating the Distributed Complexity" — Università di Bologna, seminar / lecture.

## Selected Internal Trainings and Workshops (JMA Wireless)

- 2020 — "XRAN Architecture — Transitioning from 4G to 5G and open fronthaul" — internal architecture training.
- 2020 — "JMA XRAN — Operations and Management" — internal O&M technical presentation.
- 2021 — "XRAN in Cloud — Lessons learnt by translating an always-changing product to a virtual, containerized, self-sustainable RAN running in Kubernetes" — RTMC training, December 2021.
- 2022 — "XRAN in Cloud" (series) — internal training variants delivered to QA, engineering, and partner lab teams across multiple JMA sites.
- 2023 — "Architecture Workshop" — internal architecture workshop, Bologna, March 2023.
- 2023 — "Architecture Workshop — R&D transfer - O&M" — internal R&D transfer / O&M workshop across Bologna, Richmond, Chicago, Boulder.
- 2023 — "PlugFest Readout — observations, risks, mitigation" — internal Architecture Team readout.
- 2026 — "Standardization — Past, present, and future strategic assessment" — internal standards strategy briefing.
- 2026 — "Joint 3GPP / O-RAN Workshop on 6G Mgmt & Orchestration" — internal standards workshop report.
- 2026 — "AI-RAN Alliance — Technical Overview and Roadmap" — internal technical overview.
