# Источники и границы обоснования

Дата проверки технических источников: 17 ноября 2026 года. Используются официальные документы. Требования задания и исходный шаблон предоставлены пользователем; цифры проекта, бюджеты времени и выбор архитектуры являются решениями автора, а не готовыми рекомендациями из этих источников.

| ID | Источник | Что подтверждает в работе |
| --- | --- | --- |
| S1 | [Firebase: Understanding message delivery](https://firebase.google.com/docs/cloud-messaging/understand-delivery) | Различие принятых и полученных сообщений; агрегированная отчётность имеет задержки и не заменяет оперативный ACK конкретного уведомления. |
| S2 | [Firebase: Set the lifespan of a message](https://firebase.google.com/docs/cloud-messaging/customize-messages/setting-message-lifespan) | Принятие FCM не равно доставке; TTL ограничивает хранение, collapse key может заменить ожидающее сообщение. TTL уменьшает поздние доставки, но не обеспечивает межканальную дедупликацию. |
| S3 | [Twilio: Message resource — status values](https://www.twilio.com/docs/messaging/api/message-resource#message-status-values) | `accepted`, `sent` и `delivered` имеют разный смысл; delivery receipt зависит от оператора и доступных подтверждений. Twilio здесь пример контракта, не выбранный поставщик для банка. |
| S4 | [Apache Kafka: Design — Message Delivery Semantics](https://kafka.apache.org/44/design/design/#message-delivery-semantics) | Повторная обработка и границы exactly-once; внешняя система требует собственного согласования результатов. Kafka transaction не охватывает обычный HTTP-вызов SMS. |
| S5 | [Temporal: Activity Definition — Idempotency](https://docs.temporal.io/activity-definition#idempotency) | Activities должны допускать повторное выполнение; завершённые шаги не вызываются заново при replay, но потерянный результат может привести к повтору activity. |
| S6 | [PostgreSQL: SELECT — locking clause](https://www.postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE) | `FOR UPDATE SKIP LOCKED` подходит для нескольких обработчиков queue-like таблицы. Сам по себе не решает lease, справедливость, внешние side effects и бизнес-дедупликацию. |
| S7 | [PostgreSQL: Synchronous Replication](https://www.postgresql.org/docs/current/warm-standby.html#SYNCHRONOUS-REPLICATION) | Условия ожидания standby и компромисс сохранности/доступности. Автоматический failover и fencing — отдельные требования архитектуры. |
| S8 | [Temporal: Understanding Temporal](https://docs.temporal.io/evaluate/understanding-temporal) | Разделение Service/Workers, сохранение истории, durable timers, persistence и восстановление процесса. Не подтверждает достижение нашей нагрузочной цели без тестов. |
| S9 | [Amazon SES: Delivery event](https://docs.aws.amazon.com/ses/latest/dg/event-publishing-retrieving-sns-contents.html#event-publishing-retrieving-sns-contents-delivery-object) | Email delivery — передача серверу получателя; это отличается от прочтения. SES — пример семантики, а не выбранный поставщик. |
| S10 | [Temporal: Retry Policies](https://docs.temporal.io/encyclopedia/retry-policies) | У activities есть автоматические retries; для внешней отправки их нужно настроить согласно идемпотентности и дедлайну. |
| S11 | [PlantUML: Standard Library](https://plantuml.com/stdlib), [Smetana](https://plantuml.com/smetana02) | Встроенная C4-библиотека и локальный layout без отдельного Graphviz. Рендеринг не требует отправки текста диаграмм на сервер. |
| S12 | [Spring Boot: Kotlin Support](https://docs.spring.io/spring-boot/reference/features/kotlin.html), [Temporal: Spring Boot integration](https://docs.temporal.io/develop/java/integrations/spring-boot-integration) | Kotlin совместим с Java-библиотеками; для Temporal Java SDK предусмотрена интеграция со Spring Boot. |
| S13 | [Podman: documentation](https://docs.podman.io/en/latest/markdown/podman.1.html) | Выбранный пользователем инструмент контейнеризации для возможного прототипа. В этой работе контейнеры не запускаются. |
| S14 | [Patroni: Replication modes](https://patroni.readthedocs.io/en/latest/replication_modes.html) | Обычный режим асинхронен; для запрета перехода к неподтверждённым записям необходимы synchronous mode/strict и безопасный выбор кандидата. Требование RPO=0 относится к подтверждённым платформой запросам в модели отказа одной зоны. |

## Материалы задания

- «Т-Образование.pdf», 8 страниц: практика 8.2, домашнее задание №4, требования к пунктам 1–8 и критерии оценки RFC.
- `rfc_template-eea98023-983f-40ce-a6cc-59afc8796642.md`: исходный шаблон RFC с метаданными, сценариями, требованиями, вариантами/этапами, сравнением и выводами. В итоговый RFC также включены продуктовый анализ, статистика и связанные задачи из оглавления шаблона.

## Что источниками не доказано

SLO 99,9% за 60 секунд, тайм-ауты 1/4/20 секунд, коэффициент пика 10, доля успешных push 95%, сроки хранения и цены в примере — проектные гипотезы. Документация технологий не гарантирует эти значения на заданном оборудовании и выбранных каналах. В RFC дан план проверки и указаны условия, при которых нужна корректировка.
