"""
Builds occupations.csv — a curated, tech-focused occupation dataset.

Source basis: occupation titles, descriptions and core competency areas are
aligned with the U.S. Department of Labor O*NET-SOC taxonomy (public domain,
https://www.onetonline.org) for the technology sector. Skill weightings
(1-5 importance) are compiled from O*NET's "Skills" and "Technology Skills"
importance ratings for the closest matching SOC codes, condensed into a
single reusable skills taxonomy for this project.

This script is a one-time data-build step — the FastAPI app reads the
resulting CSV at request time, it does not re-run this script.
"""
import csv

# Each occupation: (onet_soc_code, title, category, description, salary_low, salary_high, skills{name: weight 1-5}, interest_tags)
OCCUPATIONS = [
    dict(
        soc="15-1252.00", title="Software Developer", category="Engineering",
        description="Designs, builds and maintains applications and systems software, "
                     "translating requirements into working, maintainable code.",
        salary_low=75000, salary_high=145000,
        skills={"Python": 5, "JavaScript": 4, "Data Structures & Algorithms": 5, "Git": 5,
                "REST APIs": 4, "SQL": 3, "System Design": 3, "Problem Solving": 5,
                "CI/CD": 3, "Testing & QA": 3},
        interests=["building products", "problem solving", "software engineering"]
    ),
    dict(
        soc="15-2051.00", title="Data Scientist", category="Data & AI",
        description="Extracts insight and predictive value from data using statistics, "
                     "machine learning and experimentation.",
        salary_low=95000, salary_high=165000,
        skills={"Python": 5, "Statistics": 5, "Machine Learning": 5, "SQL": 4,
                "Data Visualization": 4, "Deep Learning": 3, "Data Structures & Algorithms": 2,
                "Communication": 3, "Big Data Tools": 2},
        interests=["data & analytics", "artificial intelligence", "research"]
    ),
    dict(
        soc="15-2051.01", title="Machine Learning Engineer", category="Data & AI",
        description="Builds, trains and productionizes ML models, bridging data science "
                     "prototypes and reliable production systems.",
        salary_low=105000, salary_high=175000,
        skills={"Python": 5, "Machine Learning": 5, "Deep Learning": 5, "TensorFlow/PyTorch": 4,
                "System Design": 3, "Cloud Platforms": 4, "Data Structures & Algorithms": 4,
                "CI/CD": 3, "Statistics": 3},
        interests=["artificial intelligence", "software engineering", "research"]
    ),
    dict(
        soc="15-1212.00", title="Information Security Analyst", category="Security",
        description="Protects systems and networks by monitoring for threats, hardening "
                     "infrastructure and responding to incidents.",
        salary_low=85000, salary_high=150000,
        skills={"Network Security": 5, "Cybersecurity Fundamentals": 5, "Risk Assessment": 4,
                "Linux": 3, "Cryptography": 3, "Penetration Testing": 3, "Compliance & Auditing": 3,
                "Incident Response": 4, "Python": 2},
        interests=["cybersecurity", "risk & compliance", "problem solving"]
    ),
    dict(
        soc="15-1211.01", title="Cloud Solutions Architect", category="Cloud & Infra",
        description="Designs scalable, resilient cloud infrastructure and guides teams "
                     "on cloud-native best practice.",
        salary_low=115000, salary_high=185000,
        skills={"Cloud Platforms": 5, "System Design": 5, "Networking": 4, "Terraform/IaC": 4,
                "Containers & Orchestration": 4, "Cybersecurity Fundamentals": 3, "Linux": 3,
                "Cost Optimization": 3, "Communication": 3},
        interests=["cloud & infrastructure", "system design", "leadership"]
    ),
    dict(
        soc="15-1244.00", title="DevOps / Site Reliability Engineer", category="Cloud & Infra",
        description="Builds the automation, monitoring and delivery pipelines that keep "
                     "software shipping fast and running reliably.",
        salary_low=100000, salary_high=170000,
        skills={"CI/CD": 5, "Containers & Orchestration": 5, "Cloud Platforms": 4,
                "Linux": 4, "Terraform/IaC": 4, "Monitoring & Observability": 4,
                "Python": 3, "Networking": 3, "Incident Response": 3},
        interests=["cloud & infrastructure", "automation", "problem solving"]
    ),
    dict(
        soc="15-1211.00", title="Full-Stack Web Developer", category="Engineering",
        description="Builds both the client-facing interface and the server-side logic "
                     "of web applications end to end.",
        salary_low=70000, salary_high=135000,
        skills={"JavaScript": 5, "React/Frontend Frameworks": 5, "Node.js": 4, "SQL": 3,
                "REST APIs": 4, "HTML/CSS": 5, "Git": 4, "System Design": 2, "Testing & QA": 2},
        interests=["building products", "ui/ux", "software engineering"]
    ),
    dict(
        soc="15-1254.00", title="Mobile Application Developer", category="Engineering",
        description="Designs and builds native or cross-platform mobile apps for iOS and Android.",
        salary_low=75000, salary_high=140000,
        skills={"Mobile Development": 5, "Kotlin/Swift": 4, "React Native/Flutter": 4,
                "REST APIs": 3, "UI Design": 3, "Git": 3, "Testing & QA": 3, "Problem Solving": 3},
        interests=["building products", "ui/ux", "software engineering"]
    ),
    dict(
        soc="15-1211.02", title="Data Engineer", category="Data & AI",
        description="Builds the pipelines and warehouses that move and shape data reliably "
                     "at scale for analytics and ML.",
        salary_low=95000, salary_high=160000,
        skills={"Python": 4, "SQL": 5, "Big Data Tools": 5, "ETL Pipelines": 5,
                "Cloud Platforms": 4, "Data Warehousing": 4, "System Design": 3, "Linux": 2},
        interests=["data & analytics", "cloud & infrastructure", "automation"]
    ),
    dict(
        soc="15-2041.00", title="Business Intelligence Analyst", category="Data & AI",
        description="Turns raw business data into dashboards and insight that drive "
                     "decisions across an organization.",
        salary_low=70000, salary_high=120000,
        skills={"SQL": 5, "Data Visualization": 5, "BI Tools (Tableau/Power BI)": 5,
                "Statistics": 3, "Communication": 4, "Data Warehousing": 3, "Excel/Spreadsheets": 3},
        interests=["data & analytics", "business strategy", "communication"]
    ),
    dict(
        soc="15-1299.08", title="Cybersecurity Penetration Tester", category="Security",
        description="Simulates real-world attacks to find and report exploitable "
                     "weaknesses before adversaries do.",
        salary_low=90000, salary_high=155000,
        skills={"Penetration Testing": 5, "Network Security": 4, "Cybersecurity Fundamentals": 4,
                "Linux": 4, "Python": 3, "Cryptography": 2, "Incident Response": 2, "Communication": 3},
        interests=["cybersecurity", "problem solving", "research"]
    ),
    dict(
        soc="15-1232.00", title="QA / Test Automation Engineer", category="Engineering",
        description="Designs automated test suites and quality processes that catch "
                     "defects before they reach users.",
        salary_low=65000, salary_high=120000,
        skills={"Testing & QA": 5, "Test Automation Frameworks": 5, "Python": 3, "JavaScript": 2,
                "CI/CD": 3, "SQL": 2, "Problem Solving": 4, "Communication": 2},
        interests=["software engineering", "problem solving", "quality"]
    ),
    dict(
        soc="15-1211.03", title="Blockchain Developer", category="Engineering",
        description="Designs and implements smart contracts and decentralized applications "
                     "on blockchain platforms.",
        salary_low=95000, salary_high=165000,
        skills={"Solidity/Smart Contracts": 5, "Blockchain Fundamentals": 5, "JavaScript": 3,
                "Cryptography": 3, "System Design": 3, "Python": 2, "Testing & QA": 2},
        interests=["artificial intelligence", "software engineering", "research"]
    ),
    dict(
        soc="15-1211.04", title="AI Research Scientist", category="Data & AI",
        description="Advances the state of the art in machine learning through original "
                     "research, experimentation and publication.",
        salary_low=120000, salary_high=200000,
        skills={"Machine Learning": 5, "Deep Learning": 5, "Statistics": 5, "Python": 4,
                "TensorFlow/PyTorch": 4, "Research & Experimentation": 5, "Communication": 3},
        interests=["artificial intelligence", "research", "academia"]
    ),
    dict(
        soc="15-1199.09", title="Product Manager (Technical)", category="Product & Strategy",
        description="Owns the product roadmap, translating user and business needs into "
                     "what engineering builds next.",
        salary_low=95000, salary_high=165000,
        skills={"Product Strategy": 5, "Communication": 5, "Data Visualization": 3,
                "UX Research": 3, "Agile/Scrum": 4, "SQL": 2, "Leadership": 4, "Problem Solving": 3},
        interests=["business strategy", "leadership", "ui/ux"]
    ),
    dict(
        soc="15-1255.00", title="UX/UI Designer", category="Product & Strategy",
        description="Researches user needs and designs interfaces that are usable, "
                     "accessible and delightful.",
        salary_low=70000, salary_high=130000,
        skills={"UI Design": 5, "UX Research": 5, "Prototyping (Figma)": 5, "Wireframing": 4,
                "Communication": 4, "HTML/CSS": 2, "Visual Design Systems": 3},
        interests=["ui/ux", "building products", "research"]
    ),
    dict(
        soc="15-1244.01", title="Network Engineer", category="Cloud & Infra",
        description="Designs, implements and maintains the network infrastructure that "
                     "connects systems and services.",
        salary_low=70000, salary_high=130000,
        skills={"Networking": 5, "Network Security": 4, "Linux": 3, "Cloud Platforms": 3,
                "Monitoring & Observability": 3, "Troubleshooting": 4, "Cybersecurity Fundamentals": 3},
        interests=["cloud & infrastructure", "cybersecurity", "problem solving"]
    ),
    dict(
        soc="15-1242.00", title="Database Administrator", category="Data & AI",
        description="Keeps databases performant, available and secure, and designs schemas "
                     "that scale.",
        salary_low=75000, salary_high=135000,
        skills={"SQL": 5, "Database Design": 5, "Backup & Recovery": 4, "Linux": 3,
                "Cloud Platforms": 3, "Performance Tuning": 4, "Cybersecurity Fundamentals": 2},
        interests=["data & analytics", "cloud & infrastructure", "problem solving"]
    ),
    dict(
        soc="15-1231.00", title="Computer Systems Administrator", category="Cloud & Infra",
        description="Keeps servers, systems and internal IT infrastructure running smoothly "
                     "for an organization.",
        salary_low=60000, salary_high=110000,
        skills={"Linux": 5, "Networking": 4, "Cloud Platforms": 3, "Troubleshooting": 5,
                "Cybersecurity Fundamentals": 3, "Scripting (Bash/Python)": 3, "Monitoring & Observability": 3},
        interests=["cloud & infrastructure", "problem solving", "automation"]
    ),
    dict(
        soc="15-2099.01", title="NLP / Computer Vision Engineer", category="Data & AI",
        description="Builds systems that understand language or images, from research "
                     "prototypes to deployed models.",
        salary_low=110000, salary_high=180000,
        skills={"Deep Learning": 5, "NLP/Computer Vision": 5, "Python": 5, "TensorFlow/PyTorch": 4,
                "Machine Learning": 4, "Statistics": 3, "Research & Experimentation": 3},
        interests=["artificial intelligence", "research", "software engineering"]
    ),
]

FIELDS = ["soc", "title", "category", "description", "salary_low", "salary_high", "skills", "interests"]

def main():
    with open("occupations.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for occ in OCCUPATIONS:
            row = dict(occ)
            row["skills"] = ";".join(f"{k}:{v}" for k, v in occ["skills"].items())
            row["interests"] = "|".join(occ["interests"])
            writer.writerow(row)
    print(f"Wrote {len(OCCUPATIONS)} occupations to occupations.csv")

if __name__ == "__main__":
    main()
