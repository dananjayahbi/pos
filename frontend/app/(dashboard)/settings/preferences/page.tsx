import { redirect } from 'next/navigation';

/**
 * Redirect /settings/preferences → /settings
 * General/preference settings live at /settings.
 */
export default function SettingsPreferencesRedirect() {
  redirect('/settings');
}
