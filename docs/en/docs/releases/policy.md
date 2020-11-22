# NOC Release and Tagging Policy

## Branches

### master

`master` is main development branch. `master` is protected from changes
and populated only via Merge Requests, which have passed full Q&A process.

### release-X.Y

`release-X.Y` is branch hosting whole _Release Generation_.
_Release Generation X.Y_ is a group of releases, started with _X.Y_
and followed by _X.Y.Z_ hotfix releases.
`release-X.Y` branch is protected from changes and populated only via Merge Request,
which have passed full Q&A process.
Most of MRs on `release-X.Y` branch are *cherrypics* from MRs on `master` branch

## Tags

Following tags are usable as tower deploy branches and Docker image tags

### latest

head of [master](#master) branch

### latest-X.Y

head of :ref:`release-X.Y<releases-policy-release-X.Y>` branch

### X.Y

First release in X.Y generation on :ref:`release-X.Y<releases-policy-release-X.Y>` branch

### X.Y.Z

Hotfix releases in X.Y generation on :ref:`release-X.Y<releases-policy-release-X.Y>` branch

### stable-X.Y

Last tagged release in X.Y generation on :ref:`release-X.Y<releases-policy-release-X.Y>` branch (X.Y or last X.Y.Z)

###stable
Last tagged release in last generation
