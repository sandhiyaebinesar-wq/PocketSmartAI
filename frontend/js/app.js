const API_URL = "http://127.0.0.1:8000";


function saveToken(token) {
    localStorage.setItem("pocketsmart_token", token);
}


function getToken() {
    return localStorage.getItem("pocketsmart_token");
}


function logout() {
    localStorage.removeItem("pocketsmart_token");
    window.location.href = "index.html";
}


/* =========================
   REGISTER
========================= */

const registerForm = document.getElementById("registerForm");

if (registerForm) {

    registerForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const email = document.getElementById("registerEmail").value;
        const password = document.getElementById("registerPassword").value;
        const confirmPassword =
            document.getElementById("confirmPassword").value;

        const message =
            document.getElementById("registerMessage");


        if (password !== confirmPassword) {

            message.textContent =
                "Passwords do not match.";

            return;
        }


        try {

            const response = await fetch(
                `${API_URL}/account/register`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                }
            );


            const data = await response.json();


            if (!response.ok) {

                message.textContent =
                    data.detail || "Registration failed.";

                return;
            }


            saveToken(data.token);

            message.textContent =
                "Account created successfully!";


            setTimeout(function () {

                window.location.href =
                    "dashboard.html";

            }, 1000);


        } catch (error) {

            message.textContent =
                "Cannot connect to the server.";
        }

    });
}


/* =========================
   LOGIN
========================= */

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const email =
            document.getElementById("email").value;

        const password =
            document.getElementById("password").value;

        const message =
            document.getElementById("loginMessage");


        try {

            const response = await fetch(
                `${API_URL}/account/login`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                }
            );


            const data = await response.json();


            if (!response.ok) {

                message.textContent =
                    data.detail || "Login failed.";

                return;
            }


            saveToken(data.token);

            message.textContent =
                "Login successful!";


            setTimeout(function () {

                window.location.href =
                    "dashboard.html";

            }, 700);


        } catch (error) {

            message.textContent =
                "Cannot connect to the server.";
        }

    });
}


/* =========================
   HOME PLANNER
========================= */

const homeForm = document.getElementById("homeForm");

if (homeForm) {

    homeForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const budget =
            document.getElementById("homeBudget").value;

        const room =
            document.getElementById("room").value;

        const style =
            document.getElementById("style").value;

        const people =
            document.getElementById("people").value;

        await getRecommendation(
            "Home",
            {
                budget: budget,
                room: room,
                style: style,
                people: people
            },
            "homeMessage"
        );

    });
}


/* =========================
   PARTY PLANNER
========================= */

const partyForm = document.getElementById("partyForm");

if (partyForm) {

    partyForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const budget =
            document.getElementById("partyBudget").value;

        const eventName =
            document.getElementById("event").value;

        const guests =
            document.getElementById("guests").value;

        const theme =
            document.getElementById("theme").value;


        await getRecommendation(
            "Party",
            {
                budget: budget,
                event: eventName,
                guests: guests,
                theme: theme
            },
            "partyMessage"
        );

    });
}


/* =========================
   JEWELRY PLANNER
========================= */

const jewelryForm =
    document.getElementById("jewelryForm");

if (jewelryForm) {

    jewelryForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            const budget =
                document.getElementById(
                    "jewelryBudget"
                ).value;

            const occasion =
                document.getElementById(
                    "occasion"
                ).value;

            const metal =
                document.getElementById(
                    "metal"
                ).value;


            await getRecommendation(
                "Jewelry",
                {
                    budget: budget,
                    occasion: occasion,
                    metal: metal
                },
                "jewelryMessage"
            );

        }
    );
}


/* =========================
   GET RECOMMENDATION
========================= */

async function getRecommendation(
    planner,
    data,
    messageId
) {

    const token = getToken();

    const message =
        document.getElementById(messageId);


    if (!token) {

        message.textContent =
            "Please login first.";

        setTimeout(function () {

            window.location.href =
                "login.html";

        }, 1000);

        return;
    }


    message.textContent =
        "🤖 AI is preparing your recommendations...";


    try {

        const response = await fetch(
            `${API_URL}/planner/recommend`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },

                body: JSON.stringify({
                    planner: planner,
                    data: data
                })
            }
        );


        const result = await response.json();


        if (!response.ok) {

            message.textContent =
                result.detail ||
                "Unable to get recommendations.";

            return;
        }


        localStorage.setItem(
            "pocketsmart_result",
            JSON.stringify(result)
        );


        window.location.href =
            "results.html";


    } catch (error) {

        message.textContent =
            "Cannot connect to the backend server.";

    }
}


/* =========================
   DISPLAY RESULTS
========================= */

const resultsContainer =
    document.getElementById(
        "resultsContainer"
    );


if (resultsContainer) {

    const savedResult =
        localStorage.getItem(
            "pocketsmart_result"
        );


    if (savedResult) {

        const result =
            JSON.parse(savedResult);


        const summary =
            document.getElementById(
                "resultSummary"
            );


        if (summary) {

            summary.textContent =
                result.summary || "";
        }


        if (result.items) {

            result.items.forEach(function (item) {

                const card =
                    document.createElement("div");

                card.className =
                    "result-card";


                card.innerHTML = `

                    <h3>${item.name || "Recommendation"}</h3>

                    <p>
                        Category:
                        ${item.category || "-"}
                    </p>

                    <p class="price">
                        ₹${item.price || 0}
                    </p>

                    <p>
                        Platform:
                        ${item.platform || "-"}
                    </p>

                    <p>
                        ${item.reason || ""}
                    </p>

                    ${
                        item.link
                        ?
                        `<a
                            href="${item.link}"
                            target="_blank"
                            class="btn"
                        >
                            View Product
                        </a>`
                        :
                        ""
                    }

                `;


                resultsContainer.appendChild(card);

            });

        }

    } else {

        resultsContainer.innerHTML =
            "<p>No recommendations found.</p>";

    }
}


/* =========================
   HISTORY
========================= */

const historyContainer =
    document.getElementById(
        "historyContainer"
    );


if (historyContainer) {

    loadHistory();

}


async function loadHistory() {

    const token = getToken();


    if (!token) {

        historyContainer.innerHTML =
            "<p>Please login first.</p>";

        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/history/`,
            {
                headers: {
                    "Authorization":
                        `Bearer ${token}`
                }
            }
        );


        const data =
            await response.json();


        if (!response.ok) {

            historyContainer.innerHTML =
                `<p>${data.detail || "Unable to load history."}</p>`;

            return;
        }


        if (
            !data.history ||
            data.history.length === 0
        ) {

            historyContainer.innerHTML =
                "<p>No recommendation history yet.</p>";

            return;
        }


        historyContainer.innerHTML = "";


        data.history.forEach(function (item) {

            const card =
                document.createElement("div");

            card.className =
                "history-card";


            card.innerHTML = `

                <h3>
                    ${item.planner} Planner
                </h3>

                <p>
                    Date:
                    ${item.created_at}
                </p>

                <p>
                    Recommendation saved successfully.
                </p>

            `;


            historyContainer.appendChild(card);

        });


    } catch (error) {

        historyContainer.innerHTML =
            "<p>Cannot connect to the backend server.</p>";

    }
}