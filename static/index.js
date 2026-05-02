   const API = "http://127.0.0.1:8000"
    let chart = null
    let allCompanies = []

    // Load company list on page load
    async function loadCompanies() {
      const res = await fetch(`${API}/companies`)
      const data = await res.json()
      allCompanies = data.companies
      renderList(allCompanies)
    }

    function renderList(companies) {
      const list = document.getElementById("company-list")
      list.innerHTML = ""
      companies.forEach(symbol => {
        const div = document.createElement("div")
        div.className = "company-item"
        div.textContent = symbol
        div.onclick = () => loadStock(symbol, div)
        list.appendChild(div)
      })
    }

    function filterList() {
      const query = document.getElementById("search").value.toUpperCase()
      const filtered = allCompanies.filter(s => s.includes(query))
      renderList(filtered)
    }

    // Load stock data and summary when company is clicked
    async function loadStock(symbol, el) {
      // Highlight active
      document.querySelectorAll(".company-item").forEach(d => d.classList.remove("active"))
      el.classList.add("active")

      document.getElementById("stock-title").textContent = `📊 ${symbol}`

      // Fetch summary
      const sumRes = await fetch(`${API}/summary/${symbol}`)
      const sumData = await sumRes.json()
      document.getElementById("high").textContent = "₹" + sumData["52w_high"]
      document.getElementById("low").textContent = "₹" + sumData["52w_low"]
      document.getElementById("avg").textContent = "₹" + sumData.avg_close

      // Fetch stock data
      const dataRes = await fetch(`${API}/data/${symbol}`)
      const stockData = await dataRes.json()
      const records = stockData.data

      const labels = records.map(r => r.DATE)
      const closes = records.map(r => r.CLOSE)

      // Draw chart
      if (chart) chart.destroy()
      const ctx = document.getElementById("myChart").getContext("2d")
      chart = new Chart(ctx, {
        type: "line",
        data: {
          labels: labels,
          datasets: [{
            label: `${symbol} Close Price`,
            data: closes,
            borderColor: "#38bdf8",
            backgroundColor: "rgba(56, 189, 248, 0.1)",
            fill: true,
            tension: 0.4
          }]
        },
        options: {
          responsive: true,
          plugins: { legend: { labels: { color: "white" } } },
          scales: {
            x: { ticks: { color: "#94a3b8" }, grid: { color: "#1e293b" } },
            y: { ticks: { color: "#94a3b8" }, grid: { color: "#334155" } }
          }
        }
      })
    }

    loadCompanies()