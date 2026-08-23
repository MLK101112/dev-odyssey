#!/usr/bin/env python3
"""
GitHub Builder - Daily Activity & Learning Log Engine
Generates dynamic, realistic coding/learning logs and updates activity status.
Cross-platform compatible (Windows, Linux, macOS, GitHub Actions).
"""

import argparse
import datetime
import os
import sys
from pathlib import Path

# Ensure UTF-8 output encoding across Windows/Linux/macOS
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Curated Learning Tracks & Topics
CURRICULUM = {
    "AI & Machine Learning": [
        "Transformer Architecture & Multi-Head Self-Attention Mechanisms",
        "RAG (Retrieval-Augmented Generation) with Vector DBs & Hybrid Search",
        "Fine-tuning Large Language Models with LoRA and QLoRA",
        "Deep Reinforcement Learning & Policy Gradient Methods",
        "Convolutional Neural Networks & Computer Vision Feature Extractors",
        "Model Quantization, Pruning, and ONNX Runtime Acceleration",
        "Graph Neural Networks (GNNs) for Relational Data Modeling",
        "Autonomous Multi-Agent Orchestration & Tool Calling Frameworks",
        "Diffusion Models & Latent Space Generative Representations",
        "PyTorch Custom Autograd Functions & GPU Memory Optimization"
    ],
    "Full-Stack & Cloud Architecture": [
        "Distributed Microservices Design with gRPC and Protocol Buffers",
        "Next.js App Router, Server Components & Streaming SSR Architecture",
        "Event-Driven Architecture with Apache Kafka & Event Sourcing",
        "High-Performance API Design with FastAPI and Pydantic V2",
        "Database Sharding, Partitioning, and Multi-Region Replication",
        "Advanced PostgreSQL Query Optimization, B-Tree Indexes & EXPLAIN ANALYZE",
        "Distributed Caching Strategies with Redis & Cache Invalidation Patterns",
        "WebSocket State Management & Real-Time Bi-Directional Protocols",
        "GraphQL Schema Federation & Apollo Gateway Integration",
        "Zero-Trust Cloud Security, IAM Least Privilege, and OAuth2/OIDC"
    ],
    "DevOps & Infrastructure": [
        "Kubernetes Operator Pattern & Custom Resource Definitions (CRDs)",
        "Terraform Infrastructure as Code (IaC) & State Locking with S3/DynamoDB",
        "CI/CD Pipeline Security, Ephemeral Runners & Artifact Attestation",
        "Prometheus Metrics Exporters, Alertmanager & Grafana Dashboarding",
        "Docker Multi-Stage Builds, Layer Caching, and Distroless Images",
        "Cloud-Native Service Mesh Architecture with Istio & Envoy Proxy",
        "Serverless Microservices with AWS Lambda, EventBridge, and DynamoDB",
        "Chaos Engineering & Automated Fault Injection in Staging Environments"
    ],
    "System Design & Algorithms": [
        "Distributed Consensus Algorithms (Raft & Paxos Mechanics)",
        "Distributed Rate Limiting Algorithms (Token Bucket & Leaky Bucket)",
        "Consistent Hashing & Dynamic Node Ring Rebalancing",
        "LSM-Tree Storage Engines vs B+ Trees in Modern Key-Value Stores",
        "Dynamic Programming on Trees & Advanced Bitmask State Optimization",
        "Advanced Graph Theory: Strongly Connected Components (Tarjan's/Kosaraju's)",
        "Segment Trees with Lazy Propagation & Range Query Optimizations",
        "Lock-Free Concurrency & Atomic Operations in Multi-Threaded Systems"
    ]
}

SESSION_SLOTS = [
    {"hour_range": (0, 6), "name": "Night Deep-Dive", "ist_time": "03:30 AM IST"},
    {"hour_range": (6, 12), "name": "Morning Study Session", "ist_time": "10:00 AM IST"},
    {"hour_range": (12, 17), "name": "Afternoon Coding Sprint", "ist_time": "02:00 PM IST"},
    {"hour_range": (17, 21), "name": "Evening Review & Build", "ist_time": "07:00 PM IST"},
    {"hour_range": (21, 24), "name": "Night Research & Practice", "ist_time": "10:00 PM IST"},
]

ACTION_TEMPLATES = [
    [
        "Analyzed core theoretical principles and reviewed architectural diagrams.",
        "Implemented clean prototype implementation to validate concurrency and performance.",
        "Wrote comprehensive unit and integration tests with edge-case coverage.",
        "Benchmarked performance metrics against baseline implementations."
    ],
    [
        "Investigated production documentation, RFC specifications, and engineering whitepapers.",
        "Designed modular interface contracts with type-safe schemas.",
        "Implemented real-time error handling and graceful fallback strategies.",
        "Refactored legacy modules for reduced time complexity and cleaner separation of concerns."
    ],
    [
        "Configured environment configurations and automated integration workflows.",
        "Conducted profiling session to identify memory leaks and I/O bottlenecks.",
        "Documented key findings, architecture decision records (ADR), and migration steps.",
        "Structured reproducible example repository with step-by-step verification commands."
    ],
    [
        "Completed hands-on coding drills exploring multi-threaded and asynchronous patterns.",
        "Validated schema migrations and backward compatibility across versions.",
        "Optimized algorithmic efficiency from O(N^2) to O(N log N) using tailored data structures.",
        "Compiled summary takeaways and curated reference resources for future reference."
    ],
    [
        "Evaluated tradeoffs between consistency, availability, and partition tolerance.",
        "Constructed end-to-end integration test harness simulating network partitions.",
        "Cleaned up redundant dependencies, tightened type annotations, and formatted codebase.",
        "Outlined actionable next steps for the upcoming technical milestone."
    ]
]

COMMIT_PREFIXES = [
    "docs(study)",
    "feat(learning)",
    "study(notes)",
    "chore(progress)",
    "track(daily)",
    "refactor(notes)",
    "log(session)"
]


def get_current_session(hour: int) -> dict:
    for slot in SESSION_SLOTS:
        start, end = slot["hour_range"]
        if start <= hour < end:
            return slot
    return SESSION_SLOTS[1]


def select_topic_and_category(day_of_year: int, hour: int):
    categories = list(CURRICULUM.keys())
    cat_idx = (day_of_year + (hour // 4)) % len(categories)
    category = categories[cat_idx]
    
    topics = CURRICULUM[category]
    topic_idx = (day_of_year * 3 + hour) % len(topics)
    topic = topics[topic_idx]
    
    return category, topic


def generate_entry(topic_override=None, session_override=None, target_datetime=None):
    now = target_datetime or datetime.datetime.now(datetime.timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S UTC")
    hour = now.hour
    day_of_year = int(now.strftime("%j"))

    session_info = get_current_session(hour)
    session_name = session_override or f"{session_info['name']} ({session_info['ist_time']})"

    if topic_override:
        category = "Custom Focus Track"
        topic = topic_override
    else:
        category, topic = select_topic_and_category(day_of_year, hour)

    # Pick action templates
    template_idx = (day_of_year + hour) % len(ACTION_TEMPLATES)
    actions = ACTION_TEMPLATES[template_idx]

    # Commit message
    commit_prefix = COMMIT_PREFIXES[(day_of_year * 2 + hour) % len(COMMIT_PREFIXES)]
    # Sanitize topic for commit line
    clean_topic = topic.split(" (")[0].split(" - ")[0]
    commit_msg = f"{commit_prefix}: {clean_topic} [{session_info['name'].split()[0].lower()}]"

    # Activity file single line
    activity_line = f"Last updated: {date_str} {time_str} | Session: {session_name} | Track: [{category}] {topic}\n"

    # Markdown entry block
    md_entry = (
        f"\n---\n\n"
        f"### 📌 {date_str} — {session_name}\n\n"
        f"- **Domain Track:** `{category}`\n"
        f"- **Primary Focus:** **{topic}**\n\n"
        f"#### Key Milestones & Takeaways\n"
    )
    for act in actions:
        md_entry += f"- {act}\n"
    md_entry += f"\n> *Session completed at {time_str}*\n"

    return {
        "date": date_str,
        "time": time_str,
        "session": session_name,
        "category": category,
        "topic": topic,
        "commit_msg": commit_msg,
        "activity_line": activity_line,
        "md_entry": md_entry
    }


def main():
    parser = argparse.ArgumentParser(description="GitHub Builder - Daily Activity & Learning Log Generator")
    parser.add_argument("--topic", type=str, default="", help="Custom topic to log")
    parser.add_argument("--session", type=str, default="", help="Custom session label")
    parser.add_argument("--dry-run", action="store_true", help="Print output without modifying files")
    parser.add_argument("--date", type=str, default="", help="Override date (YYYY-MM-DD HH:MM:SS)")
    args = parser.parse_args()

    target_dt = None
    if args.date:
        try:
            target_dt = datetime.datetime.strptime(args.date, "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc)
        except ValueError:
            print(f"Error: Invalid date format '{args.date}'. Expected 'YYYY-MM-DD HH:MM:SS'.", file=sys.stderr)
            sys.exit(1)

    repo_root = Path(__file__).resolve().parent.parent
    activity_file = repo_root / "activity.txt"
    log_file = repo_root / "learning-log.md"

    data = generate_entry(
        topic_override=args.topic if args.topic else None,
        session_override=args.session if args.session else None,
        target_datetime=target_dt
    )

    print("==================================================")
    print("🚀 GITHUB BUILDER - GENERATED LOG SESSION")
    print("==================================================")
    print(f"Date & Time : {data['date']} {data['time']}")
    print(f"Session     : {data['session']}")
    print(f"Category    : {data['category']}")
    print(f"Topic       : {data['topic']}")
    print(f"Commit Msg  : {data['commit_msg']}")
    print("==================================================")

    if args.dry_run:
        print("\n[DRY RUN MODE] No files were updated.\n")
        print("--- ACTIVITY FILE PREVIEW ---")
        print(data["activity_line"].strip())
        print("\n--- LEARNING LOG PREVIEW ---")
        print(data["md_entry"])
        return

    # Update activity.txt
    with open(activity_file, "w", encoding="utf-8") as f:
        f.write(data["activity_line"])
    print(f"✓ Updated {activity_file.name}")

    # Append to learning-log.md
    if not log_file.exists():
        initial_header = (
            "# 📚 Continuous Learning & Engineering Activity Journal\n\n"
            "> An automated repository journal documenting hands-on engineering research, "
            "system architecture explorations, and algorithmic practices.\n\n"
            "## 📊 Learning Overview\n\n"
            "| Track | Focus Areas |\n"
            "| :--- | :--- |\n"
            "| **AI & Machine Learning** | LLM Fine-tuning, RAG, Multi-Agent Systems, Neural Nets |\n"
            "| **Full-Stack & Cloud Architecture** | Microservices, Next.js, Distributed Caching, Security |\n"
            "| **DevOps & Infrastructure** | Kubernetes, Terraform IaC, Observability, CI/CD |\n"
            "| **System Design & Algorithms** | Distributed Consensus, Rate Limiting, Advanced Graph Theory |\n\n"
            "## 📝 Activity Timeline\n"
        )
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(initial_header)

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(data["md_entry"])
    print(f"✓ Appended entry to {log_file.name}")

    # Write commit message for CI/CD script consumption
    commit_msg_paths = [
        Path("/tmp/commit_msg.txt"),
        repo_root / ".commit_msg.tmp"
    ]
    for p in commit_msg_paths:
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(data["commit_msg"])
            break
        except Exception:
            continue

    print("✓ Successfully recorded build session.")


if __name__ == "__main__":
    main()
