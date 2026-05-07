# Experience

## JMA Wireless

### Director, Software Architecture — Aug 2024 – present

Bologna metropolitan area, Italy

Defines and drives technology strategy and architecture direction across carrier, enterprise, and federal market segments, with focus on research initiatives, standards engagement, and system architecture for DAS/RAN convergence.

**Key work:**

- Built a strategic standards-engagement proposal for JMA, recommending a sustainable 3GPP/O-RAN monitoring and participation model with FTE justification and working-group prioritization.
- Continued DAS 3.0/Jazz architecture support: vPOI PTP change management, FRS updates, DAS-126 timing feature ownership, and integration validation (PTP/SyncE, G.8275.1, DHCP/NETCONF call-home).
- Led DAS 3.0/NG2 architecture planning covering RF-to-eCPRI POI, O-RAN POI variants (CatA-to-CatA, CatB-to-CatA), RU/switch/supervisor integration, and PoC framing with accelerated summer feasibility checkpoint.
- Drove advanced development inputs for BBU and platform evolution: X-Cast, Distributed Massive MIMO, DPDK/VPP-based data plane, appliance/bare-metal/immutable OS concepts (Yocto, bootc, MicroShift).
- Escalated and structured Red Hat/OCP technical issues affecting XRAN/current product releases; evaluated RHEL for Edge, bootc, and MicroShift for DAS/Jazz deployments.
- Provided system architecture guidance on XRAN networking: link aggregation, Linux bridge limitations for F1-U, SR-IOV implications, and redundancy/capacity design guidelines.
- Drove XRAN/architecture governance architecture governance including the current major release.01/SR-05 SRS/PRD alignment and Red Hat OpenShift PoCs (XRAN on OCP, IPSec 6WIND router on OCP).
- Advanced Red Hat/OCP and AI-platform strategy: CaaS layer assessment comparing Red Hat, Wind River, and VMware; AI for RHEL/RHOCP evaluation; AIOps and SMO-like OCP platform framing.
- Structured the GitHub Copilot / DAS 3.0 AI pilot with governance, KPIs, monthly checkpoints, and management-facing material.
- Continued O-RAN/6G strategic tracking, including WG11 change requests, nGRG 6G workshop inputs, and O-Cloud technical strategy.
- Coordinated 2025 research/university collaboration pipeline with Università di Bologna and Saint Louis University; delivered network automation teaching material and edge-computing seminars.
- Prepared and delivered ENS 2024 keynote: "Smooth sailing ahead? Navigating the Edge challenges, and preparing to correct the course."

### Principal Software Architect — Feb 2023 – Aug 2024

Bologna metropolitan area, Italy

Defined mid-term and long-term product architecture direction for the XRAN portfolio, with scope expanding toward system-of-systems ownership anticipating DAS and Jazz convergence.

**Key work:**

- Formalized XRAN load and performance testing for each major release (starting the current major release), expanding scope to include UEs per cell, CU-CP/CU-UP scalability, gNB-DUs per CU, and system topology limits. Established System Dimensioning Guidelines as a formal G3 milestone deliverable.
- Proposed and coordinated the XRAN Plugfest program as a structured integration feedback mechanism, with plugfest timing tied to development sprints and architecture workshops. On-site lab work in Boulder (May 2023) supported integration validation and direct feedback from development and performance engineers.
- Coordinated multiple technical sessions with Fibrolan around the Sync Controller, including on-site validation in Bologna with architecture, QA, and system stakeholders.
- Framed CaaS productization as a comparative architecture topic across AWS EKS-A, Rancher/SUSE, and SpectroCloud Palette, focusing on what could be productized, supported, automated, and operated.
- Authored a detailed Red Hat OpenShift work plan splitting the effort into phases: manufacturing, air-gap installation, BBU workloads, networking, security, monitoring, and documentation.
- Drove 6WIND renewal and alternatives analysis for the current major release IPSec needs (Cisco VPP/fd.io, Rambus IPSec toolkit, strongSwan with DPDK fastpath).
- Contributed to O-Cloud technical strategy and NTIA federal market platform development.
- Expanded university and research collaboration with Università di Bologna and Saint Louis University.

### Manager, 5G O&M and Cloud — Sep 2021 – Feb 2023

Bologna metropolitan area, Italy

Led a team of ten engineers through the cloud transition of the XRAN portfolio, with responsibility expanding into O-RAN management, timing architecture, vendor interoperability, and field-readiness concerns.

**Key work:**

- Defined concrete NETCONF/YANG requirements for switch management covering configuration, L2/L3 interfaces, VLANs, timing (GNSS, PTP, SyncE), QoS (DSCP, PCP), mirroring, fault management, and performance measurements. Pushed for OpenConfig YANG model adoption for multi-vendor consistency across Fibrolan, Cisco, and Ciena.
- Elevated timing architecture (PTP, SyncE, GNSS) from optional enhancement to gating prerequisite for field deployment. Fibrolan approval was conditioned on NETCONF/YANG-based O&M, management bug fixes, roadmap commitments, FEC on SFP28, and QA traffic stress testing.
- Managed vendor interoperability directly: coordinated QA to validate Fibrolan switches under production-level traffic; structured Ciena interop discussions to align product portfolios before engineering engagement.
- Drove practical multi-vendor O-RU integration analysis across MTI, Fujitsu, Mavenir, and JMA O-RAN radios, exposing the gap between nominal O-RAN compliance and what was required for field operation.
- Supported Wind River WRCP production deployment for a major APAC operator, resolving containerd/SR-IOV/Mellanox NIC issues; authored containerization platforms analysis comparing VMware Tanzu, Wind River WRCP, Red Hat OpenShift/OKD, and internal Kubernetes.
- Led Juniper/a European operator Security Gateway integration, debugging certificate trust chains, AutoVPN behavior, and strongSwan configuration alignment.
- Drove 6WIND IPSec benchmarking (9.1 Gbps achieved on 10 Gbps link vs 1.6 Gbps with strongSwan).
- Assessed CaaS platform landscape: AWS EKS-A/Snowball Edge, SUSE/Rancher, Intel FlexRAN, and NVIDIA/Mellanox NIC strategy consolidation.
- Routed Fibrolan technical training (PTP theory, timing troubleshooting, switch configuration) to QA and development teams.

### System Architect — Apr 2019 – Sep 2021

Bologna, Italy

Primary technical reference for XRAN virtualization and containerization feasibility, bridging infrastructure experimentation with real BBU software behavior and performance constraints.

**Key work:**

- Continued and deepened the cloud-native XRAN program: systematic evaluation of BBU execution across bare metal, VMs, and containers, with focus on performance degradation sources (scheduler behavior, interrupt handling, PCIe access, CPU pinning).
- Formalized the architectural separation between BBU real-time critical paths and ancillary services, establishing that not all BBU-related software must share the same execution model.
- Investigated low-latency data-plane options (InfiniBand/RDMA vs Ethernet/DPDK) and their long-term architectural implications; established that data-plane choices would strongly constrain future architecture.
- Identified limitations of vanilla Kubernetes for XRAN use cases (latency, NUMA locality, hardware affinity) and documented these as architectural risks.
- Built Prometheus-based monitoring and benchmarking practices for containerized XRAN, correlating system-level metrics with BBU performance.
- Built deep Cisco NCS 540 PTP configuration expertise for G.8275.1 and G.8275.2 profiles, including Grandmaster and Boundary Clock use cases. Managed NCS 540 deployment across BTC, RTC, a European operator lab, and Vodafone-related environments.
- Started MTI O-RU M-Plane integration, translating generic O-RAN WG4 expectations into concrete NETCONF integration questions.
- Evaluated NVIDIA/Mellanox ConnectX-6 Dx NICs (PPS in/out, PCIe 4.0, crypto) and performed PTP T-BC/T-SC testing.
- Led Cisco Luminet lab integration tests (multi-operator configuration, VLAN isolation, DSCP/QoS through IPSec tunnels), Cisco CBRS project support, and Cisco Paris lab setup for O&M/NSO integration.
- Acted as bridge between European and US XRAN teams, aligning assumptions around BBU execution, virtualization constraints, and deployment expectations through combined on-site lab windows and remote collaboration.
- Consolidated containerized XRAN work into reproducible, automation-friendly setups during COVID-era constraints, shifting emphasis from experimentation to operational robustness and repeatability.

### Networking System Design Engineer — Jul 2018 – Apr 2019

Bologna, Italy

Joined JMA Wireless to explore cloud-native execution models for the XRAN baseband processing software, working under a research-mode mandate without product-delivery pressure.

**Key work:**

- Completed the first PoCs of XRAN running in Docker containers (Sep–Nov 2018), establishing the initial containerized BBU execution path including container topology, Linux namespaces, cgroups, device access, and PCIe visibility.
- Built the first Kubernetes-based experimentation environment for XRAN components.
- Conducted full InfiniBand/RDMA analysis and validation as a low-latency data-plane option for XRAN inter-node communication (Aug–Sep 2018).
- Contributed to provisional patent ID-2058 on Kubernetes/container orchestration for BBU.
- Evaluated OpenStack and Kubernetes networking suitability for telecom-grade workloads, concluding that default cloud-networking assumptions were insufficient for XRAN latency and determinism requirements.

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
