document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    const channelId = urlParams.get('id');

    if (channelId) {
        // Fetch channel details from the API with the specific id
        fetch(`https://alameed-api.alameedtv.workers.dev/channel?id=${channelId}`)
            .then(response => response.json())
            .then(async data => {
                if (data.status === "success" && data.data) {
                    const channel = data.data;
                    const manifestUri = channel.file;

                    const video = document.getElementById('video');
                    const ui = video['ui'];

                    // Ensure ui is defined before using it
                    if (ui) {
                        const config = {
                            'seekBarColors': {
                                base: 'rgba(255,255,255,.2)',
                                buffered: 'rgba(255,255,255,.4)',
                                played: 'rgb(255,0,0)',
                            },
                            'enableTooltips': true,
                        };
                        ui.configure(config);
                        const controls = ui.getControls();
                        const player = controls.getPlayer();

                        // Attach player and UI to the window for debugging
                        window.player = player;
                        window.ui = ui;

                        // Handle errors
                        player.addEventListener('error', event => {
                            console.error('Player error:', event.detail);
                        });
                        controls.addEventListener('error', event => {
                            console.error('UI error:', event.detail);
                        });

                        try {
                            // Configure player options
                            if (channel.type === 'mpd') {
                                player.configure({
                                    drm: {
                                        clearKeys: {
                                            [channel.keyId]: channel.key,
                                        },
                                    },
                                });
                            }

                            await player.load(manifestUri);
                            console.log('The video has now been loaded!');
                        } catch (error) {
                            console.error('Error loading video:', error);
                        }
                    } else {
                        console.error('UI not found for the video element');
                    }
                } else {
                    console.error('Channel not found');
                }
            })
            .catch(error => console.error('Error fetching channel details:', error));
    } else {
        console.error('Channel ID not provided');
    }
});
