document.getElementById("aiButton").addEventListener("click", async () => {

    const data = {

        model: document.getElementById("model").value,

        line: document.getElementById("line").value,

        process: document.getElementById("process").value,

        category: document.getElementById("category").value,

        defect: document.getElementById("defect").value,

        cause: document.getElementById("cause").value

    };

    const response = await fetch("/analisar", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(data)

    });

    const result = await response.json();

    document.getElementById("action").value = result.action;

});