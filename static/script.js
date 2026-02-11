async function lockPortrait() {
  try {
    // Some browsers require entering fullscreen first
    if (document.documentElement.requestFullscreen) {
      await document.documentElement.requestFullscreen();
    }
    await screen.orientation.lock('portrait');
  } catch (error) {
    console.error("Orientation lock failed:", error);
  }
}