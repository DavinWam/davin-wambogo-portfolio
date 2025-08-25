document.addEventListener("DOMContentLoaded", function () {
    // Array of game details
    const games = [
        { title: "BLADES ON ICE", link: "blades_on_ice.html", image: "../thumbnails/thumbnail_blades_on_ice.png" },
        { title: "ENYA'S JOURNEY", link: "enyas_journey.html", image: "../thumbnails/thumbnail_enyas_journey.jpg" },
        { title: "SCALE THE BEAST", link: "scale_the_beast.html", image: "../thumbnails/thumbnail_scale_the_beast.png" },
        { title: "BABY STEPS", link: "baby_steps.html", image: "../thumbnails/thumbnail_baby_steps.jpg" },
        { title: "Silent Codes ", link: "silent_codes.html", image: "../thumbnails/thumbnail_silent_codes.jpg" },
        { title: "TAXES AND TENACITY", link: "taxes_and_tenacity.html", image: "../thumbnails/thumbnail_taxes_and_tenacity.png" },
        // { title: "SPACE GAME", link: "space_game.html", image: "../thumbnails/thumbnail_space_game.png" },
        { title: "GOT STEAM, PUNK?", link: "got_steam_punk.html", image: "../thumbnails/thumbnail_got_steam,_punk.jpg" },
        { title: "LAB BAT", link: "lab_bat.html", image: "../thumbnails/thumbnail_lab_bat.PNG" },
        { title: "OTHER PROJECTS", link: "OtherProjects.html", image: "../thumbnails/thumbnail_16_9.png" },
        // { title: "PENROSE", link: "penrose.html", image: "../thumbnails/thumbnail_penrose.PNG" },
        // { title: "VALDRADA", link: "valdrada.html", image: "../thumbnails/thumbnail_valdrada.jpg" },
        // { title: "LUMINAQUA ", link: "fish_animation.html", image: "../thumbnails/thumbnail_fish_animation.jpg" }

        // Add more projects as needed 
    ];

    // Function to get the filename from the URL
    function getFileName(url) {
        return url.substring(url.lastIndexOf('/') + 1);
    }

    // Get the filename of the current page
    const currentFileName = getFileName(window.location.pathname);

    // Add the current game to sessionStorage
    let visitedGames = sessionStorage.getItem('visitedGames') ? JSON.parse(sessionStorage.getItem('visitedGames')) : [];
    if (!visitedGames.includes(currentFileName)) {
        visitedGames.push(currentFileName);
        sessionStorage.setItem('visitedGames', JSON.stringify(visitedGames));
    }

       // Load games from JSON
    fetch('./games.json')
        .then(response => response.json())
        .then(games => {
            console.log("Loaded games:", games);  // For now, just print them

            // If you want to use this later, here's a working stub for thumbnail path correction
            games.forEach(game => {
                game.image = `./thumbnails/thumbnails/thumbnails/thumbnail_${game.filename}.jpg`; // or .png depending
            });

            // Continue your carousel logic here...
        })
        .catch(error => {
            console.error("Failed to load games.json:", error);
        });

    // Function to filter games
    function filterGames(gameList, visited) {
        let unvisitedGames = gameList.filter(game => !visited.includes(getFileName(game.link)));
        let visitedGames = gameList.filter(game => visited.includes(getFileName(game.link)));

        // Randomize each list
        unvisitedGames.sort(() => 0.5 - Math.random());
        visitedGames.sort(() => 0.5 - Math.random());

        // Combine unvisited and visited games
        let combinedGames = [...unvisitedGames, ...visitedGames];

        // Find the current game and move it to the end of the list
        const currentIndex = combinedGames.findIndex(game => getFileName(game.link) === currentFileName);
        if (currentIndex > -1) {
            const [currentGame] = combinedGames.splice(currentIndex, 1);
            combinedGames.push(currentGame);
        }

        return combinedGames;
    }

    // Get the filtered games
    const filteredGames = filterGames(games, visitedGames);

    let currentIndex = 0; // Start index for cycling games
    const gamesPerPage = 4; // Number of games to display at once
    const gameGrid = document.querySelector('.random-projects .game-grid');

    // Function to display games
    function displayGames(startIndex) {
        // Clear the game grid
        gameGrid.innerHTML = '';
        // Get the subset of games to display
        const gamesToShow = filteredGames.slice(startIndex, startIndex + gamesPerPage);

        gamesToShow.forEach(game => {
            // Skip linking to the current page if it's in the middle of the subset

                // Display as a clickable link if it's not the current page
                gameGrid.innerHTML += `
                    <a href="${game.link}" class="game">
                        <img src="${game.image}" alt="${game.title}" class="image-effect">
                        <h3><span class="title">${game.title}</span></h3>
                    </a>
                `;
            
        });

        // Add empty slots if there are less than 4 games
        if (gamesToShow.length < gamesPerPage) {
            const emptySlots = gamesPerPage - gamesToShow.length;
            for (let i = 0; i < emptySlots; i++) {
                gameGrid.innerHTML += `
                    <div class="game empty-slot">
                        <div class="image-placeholder"></div>
                    </div>
                `;
            }
        }

        // Enable or disable navigation buttons
        document.getElementById('prev-btn').disabled = (startIndex === 0);
        document.getElementById('next-btn').disabled = (startIndex + gamesPerPage >= filteredGames.length);
    }

    // Event listeners for next and previous buttons
    document.getElementById('next-btn').addEventListener('click', function () {
        if (currentIndex + gamesPerPage < filteredGames.length) {
            currentIndex += gamesPerPage;
            displayGames(currentIndex);
        }
    });

    document.getElementById('prev-btn').addEventListener('click', function () {
        if (currentIndex - gamesPerPage >= 0) {
            currentIndex -= gamesPerPage;
            displayGames(currentIndex);
        }
    });

    // Initial display of games
    displayGames(currentIndex);
});
