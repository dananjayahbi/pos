"""
Tenants utilities package.

Exports:
    From middleware_utils (request-level helpers):
        - get_tenant_from_request(request)
        - get_schema_from_request(request)
        - is_tenant_resolved(request)
        - is_public_tenant(request)

    From tenant_context (connection/thread-local context accessors):
        - get_current_tenant()        — read active tenant (thread-local + connection fallback)
        - set_current_tenant(tenant)  — activate tenant on connection + thread-local
        - tenant_context(tenant)      — context manager for temporary schema switching

    From dns_verification (custom domain DNS verification - Tasks 32-36):
        - generate_verification_token()      — UUID4-based token generation
        - get_expected_txt_value(token)       — build expected TXT record value
        - get_verification_record_name(domain) — build DNS TXT record name
        - verify_domain_dns(domain, token)   — DNS TXT record verification
        - initiate_domain_verification(domain) — start verification workflow
        - check_domain_verification(domain)  — check DNS and update status
        - update_verification_status(domain, status) — update verification state
        - update_ssl_status(domain, status)  — update SSL certificate status (Task 36)
        - check_ssl_expiry(domain)           — check SSL certificate expiry (Task 36)

    From router_utils (schema access helpers - SubPhase-07 Tasks 06-07, 12-13, 15-78):
        - get_current_schema()            — return active PostgreSQL schema name
        - is_public_schema()              — check if public schema is active
        - get_tenant_from_connection()    — return active tenant from DB connection
        - get_app_schema_type(app_label)  — classify app's schema residency
        - validate_router_order()         — verify DATABASE_ROUTERS ordering
        - get_schema_info()               — return schema context dict for debugging
        - select_schema()                 — schema selector for routing (Task 12)
        - get_default_schema()            — return default (public) schema (Task 13)
        - ensure_schema()                 — ensure valid schema with fallback (Task 13)
        - get_shared_apps()               — return shared apps list (Task 15)
        - get_tenant_apps()               — return tenant apps list (Task 16)
        - get_query_schema(app_label)     — determine query target schema (Tasks 17-18)
        - is_mixed_query_safe(a, b)       — check cross-app query safety (Task 19)
        - get_schema_from_context()       — retrieve schema with source context (Task 20)
        - handle_missing_context()        — handle missing schema with fallback (Task 21)
        - get_search_path_info()          — get search_path config info (Task 22)
        - switch_schema(schema_name)      — safely switch to a different schema (Task 23)
        - schema_context(schema_name)     — context manager for schema execution (Task 24)
        - get_request_isolation_info()    — get request isolation info (Task 25)
        - validate_schema_exists(name)    — validate schema existence (Task 26)
        - handle_invalid_schema(name)     — handle invalid schema identifiers (Task 27)
        - get_routing_logic_summary()     — programmatic routing logic summary (Task 28)
        - get_cross_schema_rules()        — cross-schema operation rules (Task 29)
        - is_cross_tenant_fk(a, b)        — check cross-tenant FK (Task 30)
        - is_cross_tenant_query(label)    — check cross-tenant query (Task 31)
        - is_shared_tenant_fk_allowed(a,b)— check tenant-to-shared FK (Task 32)
        - is_tenant_shared_fk_blocked(a,b)— check shared-to-tenant FK (Task 33)
        - get_allow_relation_rules()      — allow_relation decision tree (Task 34)
        - get_model_schema(label)         — model schema residency (Task 35)
        - compare_model_schemas(a, b)     — compare schemas between apps (Task 36)
        - raise_cross_schema_error(a, b)  — raise cross-schema error (Task 37)
        - CrossSchemaViolationError        — custom exception class (Task 38)
        - log_cross_schema_attempt(a, b)  — log violation attempts (Task 39)
        - get_raw_query_safeguards()      — raw SQL safeguards (Task 40)
        - validate_orm_relation(a, b)     — validate ORM relations (Task 41)
        - get_cross_schema_documentation() — complete cross-schema docs (Task 42)
        - get_connection_pooling_config()  — connection pooling config (Task 43)
        - get_conn_max_age_info()          — CONN_MAX_AGE documentation (Task 44)
        - get_pool_size_config()           — pool size configuration (Task 45)
        - get_connection_reuse_strategy()  — connection reuse strategy (Task 46)
        - get_schema_on_connection_info()  — schema set on connection (Task 47)
        - get_schema_reset_info()          — schema reset after request (Task 48)
        - get_connection_error_handling()  — connection error handling (Task 49)
        - get_read_replica_config()        — read replica configuration (Task 50)
        - get_read_routing_info()          — read routing to replica (Task 51)
        - get_write_routing_info()         — write routing to primary (Task 52)
        - get_replica_lag_handling()       — replica lag handling (Task 53)
        - get_connection_timeout_config()  — connection timeout config (Task 54)
        - get_connection_monitoring_info() — connection monitoring (Task 55)
        - get_connection_setup_documentation() — connection setup docs (Task 56)
        - get_query_logger_config()            — query logger config (Task 57)
        - get_query_schema_logging_info()      — schema logging info (Task 58)
        - get_query_time_logging_info()        — query time logging (Task 59)
        - get_query_metrics_config()           — query metrics config (Task 60)
        - get_per_tenant_query_tracking()      — per-tenant tracking (Task 61)
        - get_slow_query_tracking_config()     — slow query tracking (Task 62)
        - get_router_middleware_config()       — router middleware config (Task 63)
        - get_common_query_optimizations()     — common query optimizations (Task 64)
        - get_query_analyzer_config()          — query analyzer config (Task 65)
        - get_query_caching_config()           — query caching config (Task 66)
        - get_debug_toolbar_plugin_config()    — debug toolbar plugin (Task 67)
        - get_monitoring_setup_documentation() — monitoring setup docs (Task 68)
        - get_router_test_config()             — router test config (Task 69)
        - get_schema_routing_test_config()     — schema routing tests (Task 70)
        - get_cross_schema_block_test_config() — cross-schema block tests (Task 71)
        - get_connection_reuse_test_config()   — connection reuse tests (Task 72)
        - get_concurrent_request_test_config() — concurrent request tests (Task 73)
        - get_schema_fallback_test_config()    — schema fallback tests (Task 74)
        - get_integration_test_config()         — integration tests (Task 75)
        - get_performance_test_config()         — performance benchmarks (Task 76)
        - get_test_results_documentation()      — test results docs (Task 77)
        - get_initial_commit_config()           — initial commit config (Task 78)

    From provisioning_utils (provisioning flow helpers - SubPhase-09 Tasks 01-88):
        - get_provisioning_service_config()      — provisioning service (Task 01)
        - get_provisioning_interface_config()    — provisioning interface (Task 02)
        - get_provision_method_config()          — provision method (Task 03)
        - get_deprovision_method_config()        — deprovision method (Task 04)
        - get_provisioning_steps_config()        — provisioning steps enum (Task 05)
        - get_provisioning_result_config()       — provisioning result (Task 06)
        - get_provisioning_error_config()        — provisioning error (Task 07)
        - get_transaction_handling_config()      — transaction handling (Task 08)
        - get_rollback_on_failure_config()       — rollback on failure (Task 09)
        - get_provisioning_celery_task_config()  — Celery task (Task 10)
        - get_task_retry_config()                — task retry config (Task 11)
        - get_provisioning_logging_config()      — logging config (Task 12)
        - get_provisioning_events_config()       — provisioning events (Task 13)
        - get_provisioning_service_documentation() — service docs (Task 14)
        - get_schema_name_generator_config()   — schema name generator (Task 15)
        - get_schema_name_validation_config()  — schema name validation (Task 16)
        - get_schema_exists_check_config()     — schema exists check (Task 17)
        - get_create_postgresql_schema_config() — create schema (Task 18)
        - get_schema_permissions_config()      — schema permissions (Task 19)
        - get_run_tenant_migrations_config()   — run tenant migrations (Task 20)
        - get_verify_migrations_config()       — verify migrations (Task 21)
        - get_migration_failure_handling_config() — migration failure (Task 22)
        - get_cleanup_failed_schema_config()   — cleanup failed schema (Task 23)
        - get_central_schema_state_config()    — central schema state (Task 24)
        - get_schema_creation_result_config()  — schema creation result (Task 25)
        - get_schema_creation_duration_config() — schema creation duration (Task 26)
        - get_concurrent_provisioning_config() — concurrent provisioning (Task 27)
        - get_schema_provisioning_steps_documentation() — schema steps docs (Task 28)
        - get_data_seeding_service_config()   — data seeding service (Task 29)
        - get_seeding_interface_config()      — seeding interface (Task 30)
        - get_default_categories_config()     — default categories (Task 31)
        - get_default_tax_rates_config()      — default tax rates (Task 32)
        - get_default_payment_methods_config() — default payment methods (Task 33)
        - get_default_units_config()          — default units (Task 34)
        - get_default_tenant_settings_config() — default tenant settings (Task 35)
        - get_invoice_number_sequence_config() — invoice number sequence (Task 36)
        - get_order_number_sequence_config()   — order number sequence (Task 37)
        - get_default_roles_config()           — default roles (Task 38)
        - get_sample_location_config()         — sample location (Task 39)
        - get_industry_templates_config()      — industry templates (Task 40)
        - get_retail_template_config()           — retail template (Task 41)
        - get_restaurant_template_config()       — restaurant template (Task 42)
        - get_verify_seeding_complete_config()   — verify seeding complete (Task 43)
        - get_document_data_seeding_config()     — document data seeding (Task 44)
        - get_domain_service_config()              — domain service (Task 45)
        - get_subdomain_generation_config()        — subdomain generation (Task 46)
        - get_subdomain_validation_config()        — subdomain validation (Task 47)
        - get_reserved_subdomains_config()         — reserved subdomains (Task 48)
        - get_primary_domain_creation_config()     — primary domain creation (Task 49)
        - get_mark_domain_primary_config()         — mark domain primary (Task 50)
        - get_domain_cache_config()                  — domain cache config (Task 51)
        - get_domain_resolution_test_config()        — domain resolution tests (Task 52)
        - get_custom_domain_flow_config()            — custom domain flow (Task 53)
        - get_verification_token_config()            — verification token (Task 54)
        - get_cname_instructions_config()            — CNAME instructions (Task 55)
        - get_dns_propagation_monitoring_config()     — DNS propagation monitoring (Task 56)
        - get_custom_domain_verification_config()     — custom domain verification (Task 57)
        - get_domain_setup_documentation_config()     — domain setup documentation (Task 58)
        - get_admin_user_service_config()              — admin user service (Task 59)
        - get_first_admin_user_config()                — first admin user (Task 60)
        - get_secure_password_generation_config()      — secure password generation (Task 61)
        - get_admin_role_assignment_config()            — admin role assignment (Task 62)
        - get_email_confirmation_config()              — email confirmation (Task 63)
        - get_welcome_email_template_config()          — welcome email template (Task 64)
        - get_send_welcome_email_config()              — send welcome email (Task 65)
        - get_login_credentials_config()               — login credentials (Task 66)
        - get_quick_start_guide_config()               — quick start guide (Task 67)
        - get_admin_notification_config()              — admin notification (Task 68)
        - get_slack_discord_webhook_config()           — Slack/Discord webhook (Task 69)
        - get_email_delivery_tracking_config()          — email delivery tracking (Task 70)
        - get_email_failure_handling_config()           — email failure handling (Task 71)
        - get_notification_documentation_config()      — notification documentation (Task 72)
        - get_provisioning_status_model_config()        — provisioning status model (Task 73)
        - get_provisioning_status_fields_config()       — provisioning status fields (Task 74)
        - get_provisioning_error_tracking_config()      — provisioning error tracking (Task 75)
        - get_provisioning_timestamps_config()          — provisioning timestamps (Task 76)
        - get_status_update_method_config()             — status update method (Task 77)
        - get_provisioning_api_config()                 — provisioning API (Task 78)
        - get_trigger_endpoint_config()                  — trigger endpoint (Task 79)
        - get_status_endpoint_config()                   — status endpoint (Task 80)
        - get_cancel_endpoint_config()                   — cancel endpoint (Task 81)
        - get_websocket_updates_config()                 — WebSocket updates (Task 82)
        - get_admin_dashboard_view_config()              — admin dashboard view (Task 83)
        - get_metrics_collection_config()                — metrics collection (Task 84)
        - get_provisioning_tests_config()                — provisioning tests (Task 85)
        - get_full_provisioning_flow_test_config()       — full provisioning flow test (Task 86)
        - get_provisioning_initial_commit_config()       — provisioning initial commit (Task 87)
        - get_final_documentation_config()               — final documentation (Task 88)

    From migration_utils (migration strategy helpers - SubPhase-08 Tasks 01-84):
        - get_migration_review_config()          — migration review config (Task 01)
        - get_migration_commands_documentation() — migration commands docs (Task 02)
        - get_migration_directory_config()       — directory structure config (Task 03)
        - get_migration_settings_config()        — migration settings config (Task 04)
        - get_shared_apps_migration_config()     — shared apps scope config (Task 05)
        - get_tenant_apps_migration_config()     — tenant apps scope config (Task 06)
        - get_migration_helper_module_config()   — helper module config (Task 07)
        - get_migration_naming_convention()      — naming convention config (Task 08)
        - get_migration_template_config()        — migration template config (Task 09)
        - get_migration_dependencies_config()    — migration dependencies config (Task 10)
        - get_migration_check_script_config()    — check script config (Task 11)
        - get_makefile_migration_config()        — Makefile entries config (Task 12)
        - get_ci_migration_checks_config()       — CI migration checks config (Task 13)
        - get_migration_flow_documentation()     — migration flow docs (Task 14)
        - get_public_migration_command_config()  — public migration command (Task 15)
        - get_public_schema_apps_config()        — public schema apps config (Task 16)
        - get_initial_public_migration_config()  — initial public migration (Task 17)
        - get_public_tables_verification()       — public tables verification (Task 18)
        - get_public_migration_script_config()   — public migration script (Task 19)
        - get_tenant_table_updates_config()      — tenant table updates config (Task 20)
        - get_domain_table_updates_config()      — domain table updates config (Task 21)
        - get_plan_table_updates_config()        — plan table updates config (Task 22)
        - get_data_migration_template_config()   — data migration template (Task 23)
        - get_seed_initial_data_config()          — seed initial data config (Task 24)
        - get_public_tenant_creation_config()    — public tenant creation config (Task 25)
        - get_public_migration_verification_config() — public migration verification (Task 26)
        - get_migration_backup_config()          — migration backup config (Task 27)
        - get_public_migration_documentation_config() — public migration docs (Task 28)
        - get_tenant_migration_command_config()  — tenant migration command (Task 29)
        - get_tenant_schema_apps_config()        — tenant schema apps config (Task 30)
        - get_single_tenant_migration_config()   — single tenant migration (Task 31)
        - get_batch_tenant_migration_config()    — batch tenant migration (Task 32)
        - get_parallel_migration_config()        — parallel migration config (Task 33)
        - get_concurrency_limit_config()         — concurrency limit config (Task 34)
"""

from apps.tenants.utils.dns_verification import (
    check_domain_verification,
    check_ssl_expiry,
    generate_verification_token,
    get_expected_txt_value,
    get_verification_record_name,
    initiate_domain_verification,
    update_ssl_status,
    update_verification_status,
    verify_domain_dns,
)
from apps.tenants.utils.migration_utils import (
    get_additive_migrations_policy_config,
    get_all_tenants_rollback_config,
    get_batch_tenant_migration_config,
    get_ci_migration_checks_config,
    get_concurrency_limit_config,
    get_constraint_addition_config,
    get_data_migration_template_config,
    get_data_migration_test_config,
    get_default_values_required_config,
    get_domain_table_updates_config,
    get_failed_migration_handling_config,
    get_final_verification_config,
    get_forward_backward_ops_config,
    get_index_creation_config,
    get_initial_public_migration_config,
    get_large_scale_migration_test_config,
    get_large_tenant_handling_config,
    get_makefile_migration_config,
    get_migration_backup_config,
    get_migration_best_practices_config,
    get_migration_check_script_config,
    get_migration_checklist_config,
    get_migration_ci_pipeline_config,
    get_migration_commands_documentation,
    get_migration_dependencies_config,
    get_migration_directory_config,
    get_migration_dry_run_config,
    get_migration_flow_documentation,
    get_migration_helper_module_config,
    get_migration_initial_commit_config,
    get_migration_linter_config,
    get_migration_log_table_config,
    get_migration_monitoring_config,
    get_migration_naming_convention,
    get_migration_ordering_config,
    get_migration_performance_test_config,
    get_migration_review_config,
    get_migration_settings_config,
    get_migration_template_config,
    get_migration_test_suite_config,
    get_new_tenant_migration_test_config,
    get_no_column_renames_config,
    get_non_reversible_migration_config,
    get_nullable_new_columns_config,
    get_off_peak_migration_schedule_config,
    get_parallel_migration_config,
    get_parallel_migration_test_config,
    get_pg_zero_downtime_config,
    get_phased_column_removal_config,
    get_plan_table_updates_config,
    get_point_in_time_restore_config,
    get_pre_migration_backup_config,
    get_progress_tracking_config,
    get_public_migration_command_config,
    get_public_migration_documentation_config,
    get_public_migration_script_config,
    get_public_migration_test_config,
    get_public_migration_verification_config,
    get_public_schema_apps_config,
    get_public_tables_verification,
    get_public_tenant_creation_config,
    get_retry_failed_migrations_config,
    get_rollback_command_config,
    get_rollback_procedures_documentation_config,
    get_rollback_runbook_config,
    get_rollback_strategy_config,
    get_rollback_test_config,
    get_rollback_test_suite_config,
    get_seed_initial_data_config,
    get_shared_apps_migration_config,
    get_single_tenant_migration_config,
    get_single_tenant_rollback_config,
    get_staging_rollback_test_config,
    get_skip_problematic_tenants_config,
    get_tenant_apps_migration_config,
    get_tenant_data_migration_config,
    get_tenant_migration_command_config,
    get_tenant_migration_documentation_config,
    get_tenant_migration_test_config,
    get_tenant_migration_verification_config,
    get_tenant_schema_apps_config,
    get_tenant_table_updates_config,
    get_zero_downtime_documentation_config,
    get_zero_downtime_rules_config,
)
from apps.tenants.utils.middleware_utils import (
    get_schema_from_request,
    get_tenant_from_request,
    is_public_tenant,
    is_tenant_resolved,
)
from apps.tenants.utils.provisioning_utils import (
    get_admin_dashboard_view_config,
    get_admin_notification_config,
    get_admin_role_assignment_config,
    get_admin_user_service_config,
    get_central_schema_state_config,
    get_cleanup_failed_schema_config,
    get_cname_instructions_config,
    get_concurrent_provisioning_config,
    get_create_postgresql_schema_config,
    get_custom_domain_flow_config,
    get_custom_domain_verification_config,
    get_data_seeding_service_config,
    get_default_categories_config,
    get_default_payment_methods_config,
    get_default_roles_config,
    get_default_tax_rates_config,
    get_default_tenant_settings_config,
    get_default_units_config,
    get_deprovision_method_config,
    get_dns_propagation_monitoring_config,
    get_document_data_seeding_config,
    get_domain_cache_config,
    get_domain_resolution_test_config,
    get_domain_service_config,
    get_domain_setup_documentation_config,
    get_email_confirmation_config,
    get_email_delivery_tracking_config,
    get_cancel_endpoint_config,
    get_email_failure_handling_config,
    get_final_documentation_config,
    get_first_admin_user_config,
    get_full_provisioning_flow_test_config,
    get_industry_templates_config,
    get_invoice_number_sequence_config,
    get_login_credentials_config,
    get_mark_domain_primary_config,
    get_metrics_collection_config,
    get_migration_failure_handling_config,
    get_notification_documentation_config,
    get_order_number_sequence_config,
    get_primary_domain_creation_config,
    get_provision_method_config,
    get_provisioning_api_config,
    get_provisioning_celery_task_config,
    get_provisioning_error_config,
    get_provisioning_error_tracking_config,
    get_provisioning_events_config,
    get_provisioning_initial_commit_config,
    get_provisioning_interface_config,
    get_provisioning_logging_config,
    get_provisioning_result_config,
    get_provisioning_service_config,
    get_provisioning_service_documentation,
    get_provisioning_status_fields_config,
    get_provisioning_status_model_config,
    get_provisioning_steps_config,
    get_provisioning_tests_config,
    get_provisioning_timestamps_config,
    get_quick_start_guide_config,
    get_reserved_subdomains_config,
    get_restaurant_template_config,
    get_retail_template_config,
    get_rollback_on_failure_config,
    get_run_tenant_migrations_config,
    get_sample_location_config,
    get_schema_creation_duration_config,
    get_schema_creation_result_config,
    get_schema_exists_check_config,
    get_schema_name_generator_config,
    get_schema_name_validation_config,
    get_schema_permissions_config,
    get_schema_provisioning_steps_documentation,
    get_secure_password_generation_config,
    get_seeding_interface_config,
    get_send_welcome_email_config,
    get_slack_discord_webhook_config,
    get_status_endpoint_config,
    get_status_update_method_config,
    get_subdomain_generation_config,
    get_subdomain_validation_config,
    get_task_retry_config,
    get_transaction_handling_config,
    get_trigger_endpoint_config,
    get_verification_token_config,
    get_verify_migrations_config,
    get_verify_seeding_complete_config,
    get_websocket_updates_config,
    get_welcome_email_template_config,
)
from apps.tenants.utils.router_utils import (
    CrossSchemaViolationError,
    compare_model_schemas,
    ensure_schema,
    get_allow_relation_rules,
    get_app_schema_type,
    get_common_query_optimizations,
    get_conn_max_age_info,
    get_concurrent_request_test_config,
    get_connection_error_handling,
    get_connection_monitoring_info,
    get_connection_pooling_config,
    get_connection_reuse_strategy,
    get_connection_reuse_test_config,
    get_connection_setup_documentation,
    get_connection_timeout_config,
    get_cross_schema_block_test_config,
    get_cross_schema_documentation,
    get_cross_schema_rules,
    get_current_schema,
    get_debug_toolbar_plugin_config,
    get_default_schema,
    get_initial_commit_config,
    get_integration_test_config,
    get_model_schema,
    get_monitoring_setup_documentation,
    get_per_tenant_query_tracking,
    get_performance_test_config,
    get_pool_size_config,
    get_query_analyzer_config,
    get_query_caching_config,
    get_query_logger_config,
    get_query_metrics_config,
    get_query_schema,
    get_query_schema_logging_info,
    get_query_time_logging_info,
    get_raw_query_safeguards,
    get_read_replica_config,
    get_read_routing_info,
    get_replica_lag_handling,
    get_request_isolation_info,
    get_router_middleware_config,
    get_router_test_config,
    get_routing_logic_summary,
    get_schema_fallback_test_config,
    get_schema_from_context,
    get_schema_info,
    get_schema_on_connection_info,
    get_schema_reset_info,
    get_schema_routing_test_config,
    get_search_path_info,
    get_shared_apps,
    get_slow_query_tracking_config,
    get_tenant_apps,
    get_test_results_documentation,
    get_tenant_from_connection,
    get_write_routing_info,
    handle_invalid_schema,
    handle_missing_context,
    is_cross_tenant_fk,
    is_cross_tenant_query,
    is_mixed_query_safe,
    is_public_schema,
    is_shared_tenant_fk_allowed,
    is_tenant_shared_fk_blocked,
    log_cross_schema_attempt,
    raise_cross_schema_error,
    schema_context,
    select_schema,
    switch_schema,
    validate_orm_relation,
    validate_router_order,
    validate_schema_exists,
)
from apps.tenants.utils.tenant_context import (
    get_current_tenant,
    set_current_tenant,
    tenant_context,
)
__all__ = [
    # Request-level helpers
    "get_tenant_from_request",
    "get_schema_from_request",
    "is_tenant_resolved",
    "is_public_tenant",
    # Connection/thread-local context
    "get_current_tenant",
    "set_current_tenant",
    "tenant_context",
    # DNS verification (Tasks 32-35)
    "generate_verification_token",
    "get_expected_txt_value",
    "get_verification_record_name",
    "verify_domain_dns",
    "initiate_domain_verification",
    "check_domain_verification",
    "update_verification_status",
    # SSL certificate management (Task 36)
    "update_ssl_status",
    "check_ssl_expiry",
    # Router utilities (SubPhase-07 Tasks 06-07, 12-13, 15-78)
    "get_current_schema",
    "is_public_schema",
    "get_tenant_from_connection",
    "get_app_schema_type",
    "validate_router_order",
    "get_schema_info",
    "select_schema",
    "get_default_schema",
    "ensure_schema",
    "get_shared_apps",
    "get_tenant_apps",
    "get_query_schema",
    "is_mixed_query_safe",
    "get_schema_from_context",
    "handle_missing_context",
    "get_search_path_info",
    "switch_schema",
    "schema_context",
    "get_request_isolation_info",
    "validate_schema_exists",
    "handle_invalid_schema",
    "get_routing_logic_summary",
    "get_cross_schema_rules",
    "is_cross_tenant_fk",
    "is_cross_tenant_query",
    "is_shared_tenant_fk_allowed",
    "is_tenant_shared_fk_blocked",
    "get_allow_relation_rules",
    "get_model_schema",
    "compare_model_schemas",
    "raise_cross_schema_error",
    "CrossSchemaViolationError",
    "log_cross_schema_attempt",
    "get_raw_query_safeguards",
    "validate_orm_relation",
    "get_cross_schema_documentation",
    "get_connection_pooling_config",
    "get_conn_max_age_info",
    "get_pool_size_config",
    "get_connection_reuse_strategy",
    "get_schema_on_connection_info",
    "get_schema_reset_info",
    "get_connection_error_handling",
    "get_read_replica_config",
    "get_read_routing_info",
    "get_write_routing_info",
    "get_replica_lag_handling",
    "get_connection_timeout_config",
    "get_connection_monitoring_info",
    "get_connection_setup_documentation",
    "get_query_logger_config",
    "get_query_schema_logging_info",
    "get_query_time_logging_info",
    "get_query_metrics_config",
    "get_per_tenant_query_tracking",
    "get_slow_query_tracking_config",
    "get_router_middleware_config",
    "get_common_query_optimizations",
    "get_query_analyzer_config",
    "get_query_caching_config",
    "get_debug_toolbar_plugin_config",
    "get_monitoring_setup_documentation",
    "get_router_test_config",
    "get_schema_routing_test_config",
    "get_cross_schema_block_test_config",
    "get_connection_reuse_test_config",
    "get_concurrent_request_test_config",
    "get_schema_fallback_test_config",
    "get_integration_test_config",
    "get_performance_test_config",
    "get_test_results_documentation",
    "get_initial_commit_config",
    # Provisioning utilities (SubPhase-09 Tasks 01-88)
    "get_provisioning_service_config",
    "get_provisioning_interface_config",
    "get_provision_method_config",
    "get_deprovision_method_config",
    "get_provisioning_steps_config",
    "get_provisioning_result_config",
    "get_provisioning_error_config",
    "get_transaction_handling_config",
    "get_rollback_on_failure_config",
    "get_provisioning_celery_task_config",
    "get_task_retry_config",
    "get_provisioning_logging_config",
    "get_provisioning_events_config",
    "get_provisioning_service_documentation",
    "get_schema_name_generator_config",
    "get_schema_name_validation_config",
    "get_schema_exists_check_config",
    "get_create_postgresql_schema_config",
    "get_schema_permissions_config",
    "get_run_tenant_migrations_config",
    "get_verify_migrations_config",
    "get_migration_failure_handling_config",
    "get_cleanup_failed_schema_config",
    "get_central_schema_state_config",
    "get_schema_creation_result_config",
    "get_schema_creation_duration_config",
    "get_concurrent_provisioning_config",
    "get_schema_provisioning_steps_documentation",
    "get_data_seeding_service_config",
    "get_seeding_interface_config",
    "get_default_categories_config",
    "get_default_tax_rates_config",
    "get_default_payment_methods_config",
    "get_default_units_config",
    "get_default_tenant_settings_config",
    "get_invoice_number_sequence_config",
    "get_order_number_sequence_config",
    "get_default_roles_config",
    "get_sample_location_config",
    "get_industry_templates_config",
    "get_retail_template_config",
    "get_restaurant_template_config",
    "get_verify_seeding_complete_config",
    "get_document_data_seeding_config",
    "get_domain_service_config",
    "get_subdomain_generation_config",
    "get_subdomain_validation_config",
    "get_reserved_subdomains_config",
    "get_primary_domain_creation_config",
    "get_mark_domain_primary_config",
    "get_domain_cache_config",
    "get_domain_resolution_test_config",
    "get_custom_domain_flow_config",
    "get_verification_token_config",
    "get_cname_instructions_config",
    "get_dns_propagation_monitoring_config",
    "get_custom_domain_verification_config",
    "get_domain_setup_documentation_config",
    "get_admin_user_service_config",
    "get_first_admin_user_config",
    "get_secure_password_generation_config",
    "get_admin_role_assignment_config",
    "get_email_confirmation_config",
    "get_welcome_email_template_config",
    "get_send_welcome_email_config",
    "get_login_credentials_config",
    "get_quick_start_guide_config",
    "get_admin_notification_config",
    "get_slack_discord_webhook_config",
    "get_email_delivery_tracking_config",
    "get_email_failure_handling_config",
    "get_notification_documentation_config",
    "get_provisioning_status_model_config",
    "get_provisioning_status_fields_config",
    "get_provisioning_error_tracking_config",
    "get_provisioning_timestamps_config",
    "get_status_update_method_config",
    "get_provisioning_api_config",
    "get_trigger_endpoint_config",
    "get_status_endpoint_config",
    "get_cancel_endpoint_config",
    "get_websocket_updates_config",
    "get_admin_dashboard_view_config",
    "get_metrics_collection_config",
    "get_provisioning_tests_config",
    "get_full_provisioning_flow_test_config",
    "get_provisioning_initial_commit_config",
    "get_final_documentation_config",
    # Migration utilities (SubPhase-08 Tasks 01-84)
    "get_migration_review_config",
    "get_migration_commands_documentation",
    "get_migration_directory_config",
    "get_migration_settings_config",
    "get_shared_apps_migration_config",
    "get_tenant_apps_migration_config",
    "get_migration_helper_module_config",
    "get_migration_naming_convention",
    "get_migration_template_config",
    "get_migration_dependencies_config",
    "get_migration_check_script_config",
    "get_makefile_migration_config",
    "get_ci_migration_checks_config",
    "get_migration_flow_documentation",
    "get_public_migration_command_config",
    "get_public_schema_apps_config",
    "get_initial_public_migration_config",
    "get_public_tables_verification",
    "get_public_migration_script_config",
    "get_tenant_table_updates_config",
    "get_domain_table_updates_config",
    "get_plan_table_updates_config",
    "get_data_migration_template_config",
    "get_seed_initial_data_config",
    "get_public_tenant_creation_config",
    "get_public_migration_verification_config",
    "get_migration_backup_config",
    "get_public_migration_documentation_config",
    "get_tenant_migration_command_config",
    "get_tenant_schema_apps_config",
    "get_single_tenant_migration_config",
    "get_batch_tenant_migration_config",
    "get_parallel_migration_config",
    "get_concurrency_limit_config",
    "get_migration_ordering_config",
    "get_progress_tracking_config",
    "get_migration_log_table_config",
    "get_failed_migration_handling_config",
    "get_retry_failed_migrations_config",
    "get_skip_problematic_tenants_config",
    "get_tenant_data_migration_config",
    "get_large_tenant_handling_config",
    "get_tenant_migration_verification_config",
    "get_tenant_migration_documentation_config",
    "get_zero_downtime_rules_config",
    "get_additive_migrations_policy_config",
    "get_nullable_new_columns_config",
    "get_default_values_required_config",
    "get_no_column_renames_config",
    "get_phased_column_removal_config",
    "get_migration_linter_config",
    "get_pg_zero_downtime_config",
    "get_index_creation_config",
    "get_constraint_addition_config",
    "get_migration_dry_run_config",
    "get_off_peak_migration_schedule_config",
    "get_migration_monitoring_config",
    "get_zero_downtime_documentation_config",
    "get_rollback_strategy_config",
    "get_rollback_command_config",
    "get_forward_backward_ops_config",
    "get_rollback_test_config",
    "get_single_tenant_rollback_config",
    "get_all_tenants_rollback_config",
    "get_non_reversible_migration_config",
    "get_pre_migration_backup_config",
    "get_point_in_time_restore_config",
    "get_rollback_runbook_config",
    "get_staging_rollback_test_config",
    "get_rollback_procedures_documentation_config",
    "get_migration_test_suite_config",
    "get_public_migration_test_config",
    "get_tenant_migration_test_config",
    "get_parallel_migration_test_config",
    "get_rollback_test_suite_config",
    "get_data_migration_test_config",
    "get_migration_ci_pipeline_config",
    "get_new_tenant_migration_test_config",
    "get_large_scale_migration_test_config",
    "get_migration_performance_test_config",
    "get_migration_checklist_config",
    "get_migration_best_practices_config",
    "get_migration_initial_commit_config",
    "get_final_verification_config",
]
