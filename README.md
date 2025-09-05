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

After installing MindRoot and entering ANTHROPIC_API_KEY on `/admin` | Advanced | Environment Variables:

Copy `./agents/local/*` into `[mindroot install dir]/data/agents/local/`

Then, create a directory `/xfiles/soa` and copy the `soa` contents.

## Install Plugins

Make sure all recommended/required plugins are installed:

You can use `/admin` Install/Registry or `/admin` | Advanced | Plugins | Install from Github

`runvnc/ah_files`, `runvnc/ah_shell`, `runvnc/ah_think`, `runvnc/mr_md2pdf`, `runvnc/ah_look_at` (not needed unless uploading PDFs),

## Running Agent

You can use the MindRoot home page to submit a job. Select the `soa_coordinator` and model (Sonnet 4), enter '..' for instructions,
upload fact find and risk profile (may need to convert to text first if you forget to install `runvnc/ah_look_at`) and submit job.

You can view the progress in the View Session link, and result in View Result.

