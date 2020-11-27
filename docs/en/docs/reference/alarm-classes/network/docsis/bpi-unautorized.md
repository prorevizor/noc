---
uuid: 7b5bc42b-a8f9-4388-bf8e-08de73b625fb
---
# Network | DOCSIS | BPI Unautorized

## Symptoms

## Probable Causes

An unauthorized cable modem has been deleted to enforce BPI authorization for the specified cable modem. The specified cable modem was not performing BPI negotiation.

## Recommended Actions

Check the modem interface configuration for privacy mandatory, or check for errors in the TFTP configuration file.

## Variables

Variable | Description | Default
--- | --- | ---
mac | Cable Modem MAC | `:material-close:`
sid | Cable Modem SID | `:material-close:`
interface | Cable interface | `:material-close:`

## Events

### Opening Events
`Network | DOCSIS | BPI Unautorized` may be raised by events

Event Class | Description
--- | ---
`Network | DOCSIS | BPI Unautorized` | dispose
