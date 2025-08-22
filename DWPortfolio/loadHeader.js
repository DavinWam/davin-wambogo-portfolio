document.addEventListener("DOMContentLoaded", function() {
    const path = window.location.pathname;

    // Determine the page type based on the path
    let pageType;
    if (path === "/" || path.endsWith("DWPortfolio/")) {
        pageType = "root";
    } else if (path.endsWith("index.html")) {
        pageType = "index";
    } else if (path.endsWith("about.html")) {
        pageType = "about";
    } else if (path.endsWith("resume.html")) {
        pageType = "resume";
    } else {
        pageType = "subpage";
    }
    const test = "~davinwam/DWPortfolio/";
    // Print the current state
    console.log(window.location.pathname);
    console.log(test.endsWith("DWPortfolio/"));
    console.log("Current page type:", pageType);

    // Call the appropriate handler based on the page type
    switch (pageType) {
        case "root":
            handleRootPage();
            break;
        case "index":
            handleIndexPage();
            break;
        case "about":
            handleAboutPage();
            break;
        case "resume":
            handleResumePage();
            break;
        case "subpage":
            handleSubpage();
            break;
        default:
            console.error("Unknown page type:", pageType);
    }

    // Handlers for each page type
    function handleRootPage() {
        loadHeaderFooter('', 'index'); // Root and index may share similar header/footer, set activePage as 'index'
        console.log("Handling Root Page");
    }

    function handleIndexPage() {
        loadHeaderFooter('', 'index');
        console.log("Handling Index Page");
    }

    function handleAboutPage() {
        loadHeaderFooter('', 'about');
        console.log("Handling About Page");
    }

    function handleResumePage() {
        loadHeaderFooter('', 'resume');
        console.log("Handling Resume Page");
    }

    function handleSubpage() {
        loadHeaderFooter('../', 'subpage');
        console.log("Handling Subpage");
    }

    // Load header and footer with a specified base path
    function loadHeaderFooter(basePath, activePage) {
        document.getElementById("header-container").innerHTML = `
            <div class="text-container">
                <h1 style="white-space: nowrap;">
                    <span class="highlight">Davin Wambogo</span>
                    <span class="blinking-pipe" style="color: white;">|</span>
                    Game Designer
                </h1>
            </div>

            <nav>
                <ul>
                    <li><a href="${basePath}index.html" class="nav-button ${activePage === 'index' ? 'current-page' : ''}">Projects</a></li>
                    <li><a href="${basePath}about.html" class="nav-button ${activePage === 'about' ? 'current-page' : ''}">About</a></li>
                    <li><a href="${basePath}resume.html" class="nav-button ${activePage === 'resume' ? 'current-page' : ''}">Resume</a></li>
                </ul>
            </nav>
        `;

        document.getElementById("footer-container").innerHTML = `
            <div class="social-buttons">
                <a href="https://www.linkedin.com/in/davin-wambogo/" target="_blank" class="social-button">
                    <img src="socialButton (2).png" alt="LinkedIn" class="social-icon linkedin-icon">
                </a>
                <a href="https://deditch.itch.io" target="_blank" class="social-button">
                    <img src="socialButton (3).png" alt="Itch" class="social-icon itch-icon">
                </a>
                <a href="mailto:davinwambogo@gmail.com" class="social-button">
                    <img src="socialButton (1).png" alt="Email" class="social-icon email-icon">
                </a>
            </div>

            <footer>
                <p>Davin Wambogo - Student Game Designer</p>
            </footer>
        `;
    }
});
