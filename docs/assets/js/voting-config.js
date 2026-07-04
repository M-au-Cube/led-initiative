/**
 * Configuration du système de vote LED.
 *
 * Mode "local" : votes stockés localement (démonstration, pas d'agrégation globale).
 * Mode "supabase" : votes agrégés via Supabase (recommandé en production).
 *
 * Pour activer Supabase :
 * 1. Créez un projet sur https://supabase.com
 * 2. Créez une table `votes` (measure_id TEXT, vote_type TEXT, created_at TIMESTAMPTZ)
 * 3. Copiez ce fichier vers voting-config.local.js et renseignez vos clés
 */
window.LED_VOTING_CONFIG = {
  mode: "local",

  supabase: {
    url: "",
    anonKey: "",
    table: "votes",
  },

  formEndpoint: "",
};
