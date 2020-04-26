from zerver.lib.test_classes import ZulipTestCase
from zerver.lib.integrations import (
    split_fixture_path, get_fixture_and_image_paths, INTEGRATIONS, ScreenshotConfig, WebhookIntegration,
    DOC_SCREENSHOT_CONFIG, WEBHOOK_INTEGRATIONS, NO_SCREENSHOT_WEBHOOKS)

class IntegrationsTestCase(ZulipTestCase):

    def test_split_fixture_path(self) -> None:
        path = 'zerver/webhooks/semaphore/fixtures/push.json'
        integration_name, fixture_name = split_fixture_path(path)
        self.assertEqual(integration_name, 'semaphore')
        self.assertEqual(fixture_name, 'push')

    def test_get_fixture_and_image_paths(self) -> None:
        integration = INTEGRATIONS['airbrake']
        assert isinstance(integration, WebhookIntegration)
        screenshot_config = ScreenshotConfig('error_message.json', '002.png', 'ci')
        fixture_path, image_path = get_fixture_and_image_paths(integration, screenshot_config)
        self.assertEqual(fixture_path, 'zerver/webhooks/airbrake/fixtures/error_message.json')
        self.assertEqual(image_path, 'static/images/integrations/ci/002.png')

    def test_no_missing_doc_screenshot_config(self) -> None:
        webhook_names = {webhook.name for webhook in WEBHOOK_INTEGRATIONS}
        webhooks_with_screenshot_config = set(DOC_SCREENSHOT_CONFIG.keys())
        missing_webhooks = (webhook_names - webhooks_with_screenshot_config - NO_SCREENSHOT_WEBHOOKS)
        message = (
            f"These webhooks are missing screenshot config: {missing_webhooks}.\n"
            "Add them to zerver.lib.integrations.DOC_SCREENSHOT_CONFIG"
        )
        self.assertFalse(missing_webhooks, message)
