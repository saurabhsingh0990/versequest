<script lang="ts">
  // Types
  type Result = {
    song_credit: string[];
    original_lyrics: string[];
    meaning_lyrics: string[];
    tldr: string;
    themes: string[];
    imagery: string[];
    cultural_notes: string[];
    tone: string;
  };

  type ExplainPayload = {
    text: string;
    lang: 'en' | 'hi' | 'auto';
  };

  const API_URL = 'http://localhost:8000/api/explain';

  // State
  let text = '';
  let lang: ExplainPayload['lang'] = 'en';
  let loading = false;
  let errorMsg = '';
  let result: Result | null = null;

  // Helpers
  const hasItems = (arr?: unknown[]) => Array.isArray(arr) && arr.length > 0;

  async function explain() {
    errorMsg = '';
    result = null;

    const payload: ExplainPayload = { text: text.trim(), lang };

    if (!payload.text) {
      errorMsg = 'Please paste some lyrics or text.';
      return;
    }

    loading = true;
    try {
      const resp = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!resp.ok) {
        const serverText = await resp.text().catch(() => '');
        throw new Error(`Server error: ${resp.status}${serverText ? ` - ${serverText}` : ''}`);
      }

      const data = (await resp.json()) as Result;
      result = data;
    } catch (e) {
      errorMsg = e instanceof Error ? e.message : 'Unknown error';
    } finally {
      loading = false;
    }
  }
</script>

<section class="wrap">
  <div class="container">
    <h1 class="title">VerseQuest - Lyrics-to-Meaning</h1>
    <p class="subtitle">Paste lyrics, then click Explain Meaning.</p>

    <div class="stack">
      <textarea
        bind:value={text}
        placeholder="Paste lyrics here..."
        class="textarea"
        aria-label="Lyrics input"
      />
      <div class="row">
        <label class="label" for="lang">Language:</label>
        <select id="lang" bind:value={lang} class="select" aria-label="Language">
          <option value="en">English</option>
          <option value="hi">Hindi</option>
          <option value="auto">Auto</option>
        </select>
      </div>

      <button
        on:click={explain}
        disabled={loading}
        class="button"
        aria-busy={loading}
      >
        {loading ? 'Analyzing…' : 'Explain Meaning'}
      </button>

      {#if errorMsg}
        <div class="alert" role="alert">{errorMsg}</div>
      {/if}
    </div>

    {#if result}
      <div class="grid">
        <!-- ** FIX: Use #each for all array fields ** -->
        <div class="card">
          <h2 class="card-title">Song Credit</h2>
          {#if hasItems(result.song_credit)}
            <ul class="list">
              {#each result.song_credit as credit}<li>{credit}</li>{/each}
            </ul>
          {:else}
            <p class="muted">No credits provided.</p>
          {/if}
        </div>

        <div class="card">
          <h2 class="card-title">TL;DR</h2>
          <p>{result.tldr}</p>
        </div>

        <div class="card">
          <h2 class="card-title">Song Lyrics</h2>
          {#if hasItems(result.original_lyrics)}
            <ul class="list">
              {#each result.original_lyrics as line}<li>{line}</li>{/each}
            </ul>
          {:else}
            <p class="muted">No lyrics provided.</p>
          {/if}
        </div>

        <div class="card">
          <h2 class="card-title">Meaning</h2>
          {#if hasItems(result.meaning_lyrics)}
            <ul class="list">
              {#each result.meaning_lyrics as line}<li>{line}</li>{/each}
            </ul>
          {:else}
            <p class="muted">No meaning provided.</p>
          {/if}
        </div>

        

        <div class="card">
          <h3 class="card-subtitle">Themes</h3>
          {#if hasItems(result.themes)}
            <ul class="list">
              {#each result.themes as t}<li>{t}</li>{/each}
            </ul>
          {:else}
            <p class="muted">No themes found.</p>
          {/if}
        </div>

        <div class="card">
          <h3 class="card-subtitle">Imagery & Metaphors</h3>
          {#if hasItems(result.imagery)}
            <ul class="list">
              {#each result.imagery as i}<li>{i}</li>{/each}
            </ul>
          {:else}
            <p class="muted">No imagery found.</p>
          {/if}
        </div>

        <div class="card">
          <h3 class="card-subtitle">Cultural Notes</h3>
          {#if hasItems(result.cultural_notes)}
            <ul class="list">
              {#each result.cultural_notes as c}<li>{c}</li>{/each}
            </ul>
          {:else}
            <p class="muted">No cultural notes.</p>
          {/if}
        </div>

        <div class="card">
          <h3 class="card-subtitle">Tone</h3>
          <p>{result.tone}</p>
        </div>
      </div>
    {/if}
  </div>
</section>

<!-- Styles are unchanged, so they are omitted for brevity -->
<style>
  :root { --bg: #fff; --fg: #111; --muted: #666; --border: #eaeaea; --border-strong: #ddd; --brand: #111; --alert-bg: #f8d7da; --alert-fg: #842029; --alert-border: #f5c2c7; }
  .wrap { padding: 24px; font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; color: var(--fg); background: var(--bg); }
  .container { max-width: 800px; margin: 0 auto; }
  .title { font-size: 28px; font-weight: 600; margin: 0 0 8px 0; }
  .subtitle { color: #555; margin: 0 0 16px 0; }
  .stack { display: grid; gap: 12px; margin-bottom: 16px; }
  .textarea { width: 100%; min-height: 180px; padding: 12px; border: 1px solid var(--border-strong); border-radius: 6px; font-size: 14px; resize: vertical; }
  .row { display: flex; align-items: center; gap: 8px; }
  .label { font-size: 14px; color: #444; }
  .select { border: 1px solid var(--border-strong); border-radius: 4px; padding: 4px 8px; background: var(--bg); }
  .button { padding: 10px 14px; background: var(--brand); color: #fff; border: none; border-radius: 6px; cursor: pointer; }
  .button[disabled] { opacity: 0.7; cursor: not-allowed; }
  .alert { padding: 10px; border: 1px solid var(--alert-border); background: var(--alert-bg); color: var(--alert-fg); border-radius: 6px; }
  .grid { display: grid; gap: 16px; }
  @media (min-width: 640px) { .grid { grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); } }
  .card { padding: 12px; border: 1px solid var(--border); border-radius: 6px; background: var(--bg); }
  .card-title { font-size: 18px; font-weight: 600; margin: 0 0 6px 0; }
  .card-subtitle { font-weight: 600; margin: 0 0 6px 0; }
  .list { margin: 0; padding-left: 18px; }
  .muted { color: var(--muted); }
</style>
