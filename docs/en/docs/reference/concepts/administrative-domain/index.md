# Administrative Domain

`Administrative Domain` is a part of administrative division of
`Managed Object`. It answers to the question: "Who is responsible for
Managed Object?". Another synonym for `Administrative Domain` is
`Area of Responsibility`.

`Administrative Domains` are hierarchical by nature. Management
functions may be delegated to underlying branches. Consider example:

![Example 1](example1.svg)

Group `West` delegates management function to branches `Branch1` and `Branch2`
while group `East` - to `Branch3` and `Branch4` accordingly. Note
that `East` and `West` is not obliged to delegate all their objects
to underlying branches. Some of objects may remain on direct `East` and `West`
maintenance

## Managed Object Access

NOC limits access to `Managed Objects` on per-administrative domain basis.
[User](../user/index.md) or [Group](../group/index.md) may be granted to
zero-or-more `Administrative Domains`. Granting access to `Administrative Domain`
means that [User](../user/index.md) gets access to Managed Objects of
`Administrative Domain` and all of its descendants.

Access Limiting means [User](../user/index.md) will get access to
appropriate `Managed Objects`, their `Cards`, `Configs`, `Alarms` and `Reports`.

Consider example:

![Example 2](example2.svg)

Granting access to `West` automatically grants access to `Branch1` and `Branch2`
as well.

## Best Practices

Though you mileage may vary, consider several common practices

### Single Administrative Domain

![Single](single.svg)

Single administrative domain is good start for small installation
where all management functions carried by single department

### Functional Division

![Functional](functional.svg)

If network is maintained by several functional departments, they are
may be represented as `Administrative Domains`. Such scheme considers
`IT` need no knowledge about `Transport` and vise-versa

### Regional Division

![Regional 1](regional1.svg)

`Administrative Domain` reflects organizational branch structure. Regional
branches are responsible for their parts of network, while their head
branches fully remains control over branches and own infrastructures.

Sometimes top-level `Administrative Domain` makes sense if head office
has own infrastructure and wish to remain control on over all network.

![Regional 2](regional2.svg)

If HQ has own infrastructure but not controls all network following scheme
is possible

![Regional 3](regional3.svg)

You always has option to grant access to `HQ` and `West` and `East` to user
when necessary

### Regional-Functional division

Following scheme considers each regional branch has separate divisions
for parts of their networks

![Regional-functional](regionalfunctional.svg)


### Functional-Regional Division

Following scheme differs from previous in fact that appropriate regional
structural departments are managed by appropriate structural departments,
not by regional branches

![Functional-Regional](functionalregional.svg)

