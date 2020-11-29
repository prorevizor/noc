# alarm DataStream

`alarm` [DataStream](index.md) contains summarized alarms state

## Fields

| Name                                               | Type                         | Description                                                                                        |
| -------------------------------------------------- | ---------------------------- | -------------------------------------------------------------------------------------------------- |
| id                                                 | String                       | Alarm Id                                                                                           |
| timestamp                                          | String                       | ISO 8601 timestamp (i.e. YYYY-MM-DDTHH:MM:SS) of alarm rising                                      |
| clear_timestamp                                    | String                       | ISO 8601 timestamp (i.e. YYYY-MM-DDTHH:MM:SS) of alarm clearange (for closed alarms only)          |
| severity                                           | Integer                      | Alarm severity                                                                                     |
| root                                               | String                       | ID of root alarm (for consequences only)                                                           |
| object                                             | Object :material-arrow-down: | Managed Object                                                                                     |
| :material-arrow-right: id                          | String                       | Managed Object's ID                                                                                |
| :material-arrow-right: object_profile              | Object :material-arrow-down: | Managed Object Profile                                                                             |
| :material-arrow-right: :material-arrow-right: id   | String                       | Managed Object Profile's ID                                                                        |
| :material-arrow-right: :material-arrow-right: name | String                       | Managed Object Profile's Name                                                                      |
| :material-arrow-right: remote_system               | Object :material-arrow-down: | Managed Object's [Remote System](../../../reference/concepts/remote-system/index.md) (if imported) |
| :material-arrow-right: :material-arrow-right: id   | String                       | Remote System's ID                                                                                 |
| :material-arrow-right: :material-arrow-right: name | String                       | Remote System's Name                                                                               |
| :material-arrow-right: remote_id                   | String                       | Managed Object's ID in Remote System (if any)                                                      |
| alarm_class                                        | String                       | Alarm Class                                                                                        |
| :material-arrow-right: id                          | String                       | Alarm Class' ID                                                                                    |
| :material-arrow-right: name                        | String                       | Alarm Class' Name                                                                                  |
| vars                                               | Object :material-arrow-down: | Key-value dictionary of alarm's variables                                                          |
| reopens                                            | Integer                      | Number of alarm's reopens                                                                          |
| escalation                                         | Object :material-arrow-down: | Escalation data (if escalated)                                                                     |
| :material-arrow-right: timestamp                   | String                       | Escalation timestamp in ISO 8601 format                                                            |
| :material-arrow-right: tt_system                   | Object :material-arrow-down: | TT System to escalate                                                                              |
| :material-arrow-right: :material-arrow-right: id   | String                       | TT System's ID                                                                                     |
| :material-arrow-right: :material-arrow-right: name | String                       | TT System's name                                                                                   |
| :material-arrow-right: error                       | String                       | Escalation error text (if any)                                                                     |
| :material-arrow-right: tt_id                       | String                       | TT ID                                                                                              |
| :material-arrow-right: close_timestamp             | String                       | Escalation closing timestamp in ISO 8601 format (if closed)                                        |
| :material-arrow-right: close_error                 | String                       | Escalation closing error text (if any)                                                             |
| direct_services                                    | Object :material-arrow-down: | Summary of services directly affected by alarm                                                     |
| :material-arrow-right: profile                     | Object :material-arrow-down: | Service Profile                                                                                    |
| :material-arrow-right: :material-arrow-right: id   | String                       | Service Profile's ID                                                                               |
| :material-arrow-right: :material-arrow-right: name | String                       | Service Profile's name                                                                             |
| :material-arrow-right: summary                     | Integer                      | Number of affected services                                                                        |
| total_services                                     | Object :material-arrow-down: | Summary of services directly affected by alarm and all consequences                                |
| :material-arrow-right: profile                     | Object :material-arrow-down: | Service Profile                                                                                    |
| :material-arrow-right: :material-arrow-right: id   | String                       | Service Profile's ID                                                                               |
| :material-arrow-right: :material-arrow-right: name | String                       | Service Profile's name                                                                             |
| :material-arrow-right: summary                     | String                       | Number of affected services                                                                        |
| direct_subscribers                                 | Object :material-arrow-down: | Summary of subscribers directly affected by alarm                                                  |
| :material-arrow-right: profile                     | Object :material-arrow-down: | Subscriber Profile                                                                                 |
| :material-arrow-right: :material-arrow-right: id   | String                       | Subscriber Profile's ID                                                                            |
| :material-arrow-right: :material-arrow-right: name | String                       | Subscriber Profile's name                                                                          |
| :material-arrow-right: summary                     | Integer                      | Subscriber Profile's summary                                                                       |
| total_subscribers                                  | Object :material-arrow-down: | Summary of subscribers directly affected by alarm and all consequences                             |
| :material-arrow-right: profile                     | Object :material-arrow-down: | Subscriber Profile                                                                                 |
| :material-arrow-right: :material-arrow-right: id   | String                       | Subscriber Profile's ID                                                                            |
| :material-arrow-right: :material-arrow-right: name | String                       | Subscriber Profile's name                                                                          |
| :material-arrow-right: summary                     | Integer                      | Subscriber Profile's summary                                                                       |

## Access

[API Key](../../../reference/concepts/apikey/index.md) with `datastream:alarm` permissions
required.
