# MindRoot

[MindRoot](https://github.com/runvnc/mindroot)

# Australian SOA Financial Planning Agent for MindRoot

This is a set of related sub-agents for creating investment or insurance SOAs.

For each there is a coordinator and a set of subagents that handle subtasks.

## Insurance Agents

Coordinator: `insurance_coordinator`

Phases: `insurance_[N]..`

## Investment

Coordinator: `soa_coordinator`

Phases: `phase_[N]..`

## Install

After installing MindRoot:

Copy `./agents/local/*` into `[mindroot install dir]/data/agents/local/`

Then, create a directory `/xfiles/soa` and copy the `soa` contents.
