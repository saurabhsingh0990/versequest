<script lang="ts"> let text = ''; let lang = 'en'; let loading = false; let errorMsg = ''; let result: { tldr: string; themes: string[]; imagery: string[]; cultural_notes: string[]; tone: string; } | null = null; async function explain() { errorMsg = ''; result = null; if (!text.trim()) { errorMsg = 'Please paste some lyrics or text.'; return; } loading = true; try { const resp = await fetch('http://localhost:8000/api/explain', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text, lang }) }); if (!resp.ok) { const t = await resp.text(); throw new Error(`Server error: ${resp.status} ${t}`); } result = await resp.json(); } catch (e: any) { errorMsg = e?.message || 'Unknown error'; } finally { loading = false; } } </script> <section style="padding:24px; font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;"> <div style="max-width: 800px; margin: 0 auto;"> <h1 style="font-size: 28px; font-weight: 600; margin-bottom: 8px;">VerseQuest - Lyrics-to-Meaning</h1> <p style="color: #555; margin-bottom: 16px;">Paste lyrics, then click Explain Meaning.</p>
<div style="display: grid; gap: 12px; margin-bottom: 16px;">
  <textarea
    bind:value={text}
    placeholder="Paste lyrics here..."
    style="width: 100%; height: 180px; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;"
  />
  <div style="display: flex; align-items: center; gap: 8px;">
    <label style="font-size: 14px; color: #444;">Language:</label>
    <select bind:value={lang} style="border: 1px solid #ddd; border-radius: 4px; padding: 4px 8px;">
      <option value="en">English</option>
      <option value="hi">Hindi</option>
      <option value="auto">Auto</option>
    </select>
  </div>
  <button
    on:click={explain}
    disabled={loading}
    style="padding: 10px 14px; background:#111; color:#fff; border:none; border-radius:6px; cursor:pointer; opacity:{loading ? 0.7 : 1};"
  >
    {loading ? 'Analyzing…' : 'Explain Meaning'}
  </button>
  {#if errorMsg}
    <div style="padding: 10px; border: 1px solid #f5c2c7; background:#f8d7da; color:#842029; border-radius:6px;">{errorMsg}</div>
  {/if}
</div>

{#if result}
  <div style="display: grid; gap: 16px;">
    <div style="padding: 12px; border:1px solid #eee; border-radius:6px;">
      <h2 style="font-size: 18px; font-weight:600; margin-bottom: 6px;">TL;DR</h2>
      <p>{result.tldr}</p>
    </div>

    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px;">
      <div style="padding: 12px; border:1px solid #eee; border-radius:6px;">
        <h3 style="font-weight:600; margin-bottom:6px;">Themes</h3>
        {#if result.themes?.length}
          <ul style="margin:0; padding-left: 18px;">
            {#each result.themes as t}<li>{t}</li>{/each}
          </ul>
        {:else}<p style="color:#666;">No themes found.</p>{/if}
      </div>

      <div style="padding: 12px; border:1px solid #eee; border-radius:6px;">
        <h3 style="font-weight:600; margin-bottom:6px;">Imagery & Metaphors</h3>
        {#if result.imagery?.length}
          <ul style="margin:0; padding-left: 18px;">
            {#each result.imagery as i}<li>{i}</li>{/each}
          </ul>
        {:else}<p style="color:#666;">No imagery found.</p>{/if}
      </div>

      <div style="padding: 12px; border:1px solid #eee; border-radius:6px;">
        <h3 style="font-weight:600; margin-bottom:6px;">Cultural Notes</h3>
        {#if result.cultural_notes?.length}
          <ul style="margin:0; padding-left: 18px;">
            {#each result.cultural_notes as c}<li>{c}</li>{/each}
          </ul>
        {:else}<p style="color:#666;">No cultural notes.</p>{/if}
      </div>

      <div style="padding: 12px; border:1px solid #eee; border-radius:6px;">
        <h3 style="font-weight:600; margin-bottom:6px;">Tone</h3>
        <p>{result.tone}</p>
      </div>
    </div>
  </div>
{/if}
</div> </section>