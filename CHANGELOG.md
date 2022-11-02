# Changelog

# v0.3.6
- Feature: Support Model Management/EasService.

# v0.3.5
- Feature: Add Resource based API.

## v0.3.4
- Feature: Add CustomJob/CustomJobOperator that support run a custom PAI-DLC job in workflow.
- Feature: Pipeline support conditional/for-loop/output-parameters.

## v0.3.3
- BugFix: Support ODPS URI as input for RawArtifact.

## v0.3.2

- Feature: PAIFlow SDK support PAI-Light environment.
- BugFix

## v0.3.1
- Feature: use unregistered-operator in Pipeline.
- Feature: add a convenient method (ContainerOperator.from_scripts) to build Operator from scripts.


## v0.3.0

- Feature: Support repeated artifact in Pipeline, add class MetadataBuilder;
- Fix: Fix passing raw artifact value.
- Refactor: Use PaiFlow/AIWorkspace Tea SDK instead of POP SDK.
- Remove experimental Estimator/Transformer API.

## v0.2.0

- Feature: Support custom pipeline components with ScriptTemplate and ContainerTemplate.
- Feature: Integrate with AI Workspace service.
- Bugfix.


## v0.1.7

- Feature: Base PAI pipeline service (PaiFlow) support.
