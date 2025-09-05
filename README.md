# 2-Host Platform

🚀 **2-Host Web & Cloud Services — Integrated Network Automation Platform**

This project is an IPAM + automation tool inspired by NetBox, built with:

- **Backend:** FastAPI + SQLAlchemy + Alembic + PostgreSQL
- **Frontend:** Next.js (React) + TailwindCSS
- **Services:** Redis, Celery (for tasks), Docker Compose
- **Infrastructure goals:**
  - Sites, Devices, VRFs, VLANs, Prefixes, IPs
  - Device roles, inventory management
  - Licensing reminders
  - Cisco integration (switches, ISE, WLC)
  - ServiceNow integration
  - Network error checks (routing, unused policies, loops)

---

## Development Setup

### 1. Clone Repo
```bash
git clone https://github.com/Ayhamq/twohost-platform.git
cd twohost-platform
