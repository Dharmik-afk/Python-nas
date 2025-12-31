function videoPlayer(videoEl) {
    return {
        playing: false,
        currentTime: 0,
        duration: 0,
        volume: 1,
        muted: false,
        isBuffering: false,
        showControls: true,
        progressPercent: 0,
        bufferPercent: 0,
        isFullscreen: false,
        isScrubbing: false,
        controlsTimeout: null,

        initPlayer() {
            this.duration = videoEl.duration || 0;
            this.volume = videoEl.volume;
            this.muted = videoEl.muted;
            this.resetControlsTimer();
        },

        togglePlay() {
            if (videoEl.paused) {
                videoEl.play();
            } else {
                videoEl.pause();
            }
        },

        toggleMute() {
            this.muted = !this.muted;
            videoEl.muted = this.muted;
        },

        updateVolume() {
            videoEl.volume = this.volume;
            if (this.volume > 0) this.muted = false;
        },

        updateTime() {
            if (!this.isScrubbing) {
                this.currentTime = videoEl.currentTime;
                this.progressPercent = (this.currentTime / this.duration) * 100;
            }
        },

        updateBuffer() {
            if (videoEl.buffered.length > 0) {
                this.bufferPercent = (videoEl.buffered.end(videoEl.buffered.length - 1) / this.duration) * 100;
            }
        },

        formatTime(seconds) {
            if (!seconds || isNaN(seconds)) return '0:00';
            const h = Math.floor(seconds / 3600);
            const m = Math.floor((seconds % 3600) / 60);
            const s = Math.floor(seconds % 60);
            if (h > 0) {
                return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
            }
            return `${m}:${s.toString().padStart(2, '0')}`;
        },

        startScrubbing(e) {
            this.isScrubbing = true;
            this.scrub(e);
        },

        scrub(e) {
            if (!this.isScrubbing) return;
            const rect = e.currentTarget.getBoundingClientRect();
            const clientX = e.clientX || (e.touches ? e.touches[0].clientX : 0);
            let pos = (clientX - rect.left) / rect.width;
            pos = Math.max(0, Math.min(1, pos));
            this.progressPercent = pos * 100;
            this.currentTime = pos * this.duration;
            videoEl.currentTime = this.currentTime;
        },

        stopScrubbing() {
            this.isScrubbing = false;
            this.resetControlsTimer();
        },

        toggleFullscreen() {
            const container = videoEl.closest('.video-player-container');
            if (!document.fullscreenElement) {
                container.requestFullscreen().catch(err => {
                    console.error(`Error attempting to enable full-screen mode: ${err.message}`);
                });
                this.isFullscreen = true;
            } else {
                document.exitFullscreen();
                this.isFullscreen = false;
            }
        },

        toggleOrientation() {
            // Placeholder for Phase 2
            console.log("Orientation toggle clicked");
        },

        resetControlsTimer() {
            this.showControls = true;
            clearTimeout(this.controlsTimeout);
            if (this.playing && !this.isScrubbing) {
                this.controlsTimeout = setTimeout(() => {
                    this.showControls = false;
                }, 3000);
            }
        },

        onEnded() {
            this.playing = false;
            this.showControls = true;
        }
    };
}
