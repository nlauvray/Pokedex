document.addEventListener("DOMContentLoaded", async () => {
	const searchInput = document.getElementById("pokemon-search");
	const loadingIcon = document.getElementById("loading-icon");
	const resultsContainer = document.querySelector(".featured-pokemon");
	const pokemonCardTemplate = document.getElementById("pokemon-card-template");
	const paginationBack = document.getElementById("pagination-back");
	const paginationCurrent = document.getElementById("pagination-current");
	const paginationNext = document.getElementById("pagination-next");
	let page = 1;
	let max_page = 1;

	function debounce(func, timeout) {
		let timer;
		return (...args) => {
			clearTimeout(timer);
			timer = setTimeout(() => {
				timer = null;
				func.apply(this, [...args]);
			}, timeout);
		};
	}

	async function search(p) {
		let query = searchInput.value;
		if (query === undefined) {
			query = "";
		}

		resultsContainer.innerHTML = "";
		loadingIcon.style.display = "inline";

		const response = await fetch(`/search?query=${query}&page=${p}`);
		const { max_page: mp, pokemons } = await response.json();

		loadingIcon.style.display = "none";

		pokemons.forEach((pokemon) => {
			let pokemonCard = pokemonCardTemplate.content.cloneNode(true);
			pokemonCard.querySelector(".pokemon-name").textContent = pokemon.name;
			pokemonCard.querySelector(".pokemon-img").src = pokemon.sprites.front_default;
			pokemonCard.querySelector(".pokemon-img").alt = pokemon.name;
			resultsContainer.appendChild(pokemonCard);
			pokemonCard = resultsContainer.lastElementChild;
			pokemonCard.dataset = {};
			pokemonCard.dataset.pokemonId = pokemon.id;
			if (createPokemonCardHook !== undefined) {
				createPokemonCardHook(pokemon.id, pokemonCard);
			}
		});

		page = p;
		max_page = mp;
		paginationCurrent.textContent = `${page} sur ${max_page}`;
		paginationNext.disabled = page === max_page;
		paginationBack.disabled = page === 1;
	}

	const debouncedSearch = debounce((event) => search(1), 500);
	searchInput.addEventListener("input", debouncedSearch);

	paginationBack.addEventListener("click", async () => {
		if (page > 1) {
			page--;
			await search(page);
		}
	});

	paginationNext.addEventListener("click", async () => {
		if (page < max_page) {
			page++;
			await search(page);
		}
	});

	await search(page);
});
