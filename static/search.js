document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("pokemon-search");
  const resultsContainer = document.querySelector(".featured-pokemon");

  searchInput.addEventListener("input", async (event) => {
    const query = event.target.value;

    if (query.length > 0) {
      const response = await fetch(`/search?query=${query}`);
      const pokemons = await response.json();

      resultsContainer.innerHTML = "";

      pokemons.forEach((pokemon) => {
        const pokemonCard = document.createElement("div");
        pokemonCard.classList.add("pokemon-card-style");
        pokemonCard.innerHTML = `
          <h3>${pokemon.name}</h3>
          <img src="${ pokemon.image_url }" alt="${ pokemon.name }" >
          <a href="/pokemon/${pokemon.name}"
            <button class="btn-detail-pokemon">Voir plus</button>
          </a>
        `;
        console.log(pokemonCard.outerHTML);
        resultsContainer.appendChild(pokemonCard);
      });
    } else {
      fetchAllPokemons();
    }
  });
  fetchAllPokemons();
});
