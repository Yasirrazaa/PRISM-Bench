# PRISM Submission Guide for AgentBeats

## Quick Summary

PRISM is **fully compliant** with AgentBeats standards. Follow this guide to submit.

---

## Submission Checklist

### 1. Pre-Submission Requirements

- [ ] **Generate all 650 scenarios**
  ```bash
  python3 generator_v3_final.py          # New 5 domains (250 scenarios)
  python3 generator_level3_retrofit.py   # Level 3 for original 8 (80 scenarios)
  python3 merge_final.py                 # Merge to final 650
  ```

- [ ] **Verify scenario count**
  ```bash
  wc -l scenarios/prism_bench_final_submission.jsonl  # Should be 650
  ```

- [ ] **Test green agent locally**
  ```bash
  # Terminal 1: Start green agent
  uv run src/server.py
  
  # Terminal 2: Start baseline
  uv run baseline_agent/agent.py --port 9019
  
  # Terminal 3: Run quick test
  curl -X POST http://localhost:9009/ \
    -H "Content-Type: application/json" \
    -d '{"participants":{"evaluee":"http://localhost:9019/"},"config":{"num_scenarios":10}}'
  ```

- [ ] **Build Docker image**
  ```bash
  docker build --platform linux/amd64 -t prism-bench .
  docker run -p 9009:9009 -e GOOGLE_API_KEY=$GOOGLE_API_KEY prism-bench
  ```

### 2. GitHub Repository Setup

- [ ] Push code to GitHub
- [ ] Add `GOOGLE_API_KEY` to repository secrets (Settings → Secrets → Actions)
- [ ] Enable GitHub Actions
- [ ] Push to `main` to trigger first build
- [ ] Verify Docker image published to GitHub Container Registry

### 3. AgentBeats Platform Submission

1. **Go to**: https://agentbeats.dev
2. **Create Account** and login
3. **Submit Green Agent** with:
   - **Name**: PRISM: Pluralistic Reasoning & Identity-Specific Modeling
   - **Description**: Cultural Intelligence benchmark testing Normative Agility across 13 domains with 650 scenarios
   - **GitHub Repo**: `https://github.com/yourusername/prism-bench`
   - **Docker Image**: `ghcr.io/yourusername/prism-bench:v1.0.0`
   - **Agent Card**: Already configured in `src/server.py`

### 4. Baseline Purple Agent Evaluation

To evaluate baseline agents and show on leaderboard:

**Option A: Local Testing**
```bash
# Start green agent
uv run src/server.py

# Test all 3 baselines
for port in 9019 9020 9021; do
  uv run baseline_agent/agent.py --port $port &
  curl -X POST http://localhost:9009/ \
    -H "Content-Type: application/json" \
    -d "{\"participants\":{\"evaluee\":\"http://localhost:$port/\"},\"config\":{\"num_scenarios\":50}}"
done
```

**Option B: Submit Baselines to AgentBeats**
1. Build baseline Docker images:
   ```bash
   # Naive baseline
   docker build -f Dockerfile.baseline -t prism-baseline-naive --build-arg AGENT_FILE=baseline_agent/agent.py .
   
   # Aware baseline  
   docker build -f Dockerfile.baseline -t prism-baseline-aware --build-arg AGENT_FILE=baseline_agent/aware.py .
   
   # CoT baseline
   docker build -f Dockerfile.baseline -t prism-baseline-cot --build-arg AGENT_FILE=baseline_agent/cot.py .
   ```

2. Push to GitHub Container Registry
3. Submit as **Purple Agents** on AgentBeats
4. Run assessments using PRISM green agent

**Expected Scores:**
- Naive: 50-60%
- Aware: 70-80%
- CoT: 75-85%

### 5. Submission Form Requirements

Prepare these for the submission form:

1. **Team Info**: Your name, affiliation
2. **GitHub Repo URL**: Link to public repo
3. **Docker Image URL**: `ghcr.io/yourusername/prism-bench:v1.0.0`
4. **Short Description**: 
   > "PRISM tests Cultural Intelligence (CQ) through 650 adversarial scenarios across 13 high-friction domains. Unlike existing benchmarks, PRISM evaluates whether AI knows that 'right' and 'wrong' vary by cultural context, testing for cultural imperialism and stereotype resistance."

5. **Video Demo Link** (5 minutes):
   - Screen record: Start assessment → Show scenarios → Display results
   - Upload to YouTube (unlisted)
   - Show comparison between baseline agents

6. **Benchmark Stats**:
   - 13 Domains
   - 650 Scenarios
   - 3 Difficulty Levels
   - Automated LLM-as-Judge evaluation

---

## How Leaderboard Works

### Green Agent (Your Benchmark)
- Hosts on AgentBeats platform
- Other users run their purple agents against it
- Your benchmark appears on public leaderboard
- Scores accumulate as more agents are tested

### Purple Agents (Baselines)
- Submit as separate agents
- Run assessments via PRISM green agent
- Results appear on PRISM's leaderboard
- Shows performance range for competitors

### Leaderboard Metrics Displayed
```
Agent                    | Overall | L1 DAR | L2 SRS | L3 ICRR
-------------------------|---------|--------|--------|--------
PRISM-Baseline-Naive     | 55%     | 65%    | 60%    | 40%
PRISM-Baseline-Aware     | 75%     | 70%    | 78%    | 77%
PRISM-Baseline-CoT       | 82%     | 75%    | 85%    | 86%
Competitor Agent A       | 78%     | 72%    | 80%    | 82%
Competitor Agent B       | 85%     | 80%    | 88%    | 87%
```

---

## Technical Validation

### A2A Compliance ✅
- Accepts `assessment_request` messages
- Creates A2A tasks for participants
- Emits task updates during assessment
- Produces JSON artifacts with results
- Handles `--host`, `--port`, `--card-url` args

### Docker Requirements ✅
- Built for `linux/amd64`
- ENTRYPOINT accepts required arguments
- Environment variables for API keys
- Image pushes to GHCR

### Benchmark Quality ✅
- Novel: Tests cultural normativity (unique)
- Clear criteria: Rubric-based evaluation
- Objective: LLM-as-Judge scoring
- 650 scenarios (exceeds 20+ minimum)
- Structured JSON results
- 3 baseline agents included

---

## Post-Submission

### Phase 2 (February 2, 2026)
If selected:
- Other teams build purple agents for your benchmark
- Monitor leaderboard for new entries
- Engage with community on results
- Potential research publication

### Maintenance
- Monitor GitHub Issues
- Update scenarios if errors found
- Keep dependencies updated
- Respond to judge feedback

---

## Emergency Contacts

- **AgentBeats Support**: Check platform docs
- **Discord**: LLM Agents Discord → AgentX channel
- **Competition Info**: https://agentbeats.dev/competition

---

## Quick Command Reference

```bash
# Development
uv run src/server.py                                    # Start green agent
uv run baseline_agent/agent.py --port 9019             # Start naive baseline
uv run baseline_agent/aware.py --port 9020             # Start aware baseline
uv run pytest                                          # Run tests

# Docker
docker build --platform linux/amd64 -t prism-bench .   # Build image
docker run -p 9009:9009 -e GOOGLE_API_KEY=$KEY prism-bench  # Run container

# Generation
python3 generator_v3_final.py                          # Generate new domains
python3 generator_level3_retrofit.py                   # Generate Level 3
python3 merge_final.py                                 # Merge datasets

# Evaluation
curl -X POST http://localhost:9009/ \
  -H "Content-Type: application/json" \
  -d '{"participants":{"evaluee":"http://localhost:9019/"},"config":{"num_scenarios":50}}'
```

---

**Ready to Submit!** 🚀
