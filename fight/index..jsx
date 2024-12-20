import React from 'react';

const PokemonBattleScreen = () => {
  // Sample battle data - in a real app this would be passed as props
  const battleState = {
    opponent: {
      name: "SALAMÈCHE",
      level: 5,
      currentHP: 20,
      maxHP: 20,
      sprite: "/api/placeholder/150/150"
    },
    player: {
      name: "BULBIZARRE",
      level: 5,
      currentHP: 20,
      maxHP: 20,
      sprite: "/api/placeholder/150/150"
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-4">
      {/* Battle arena background */}
      <div className="relative h-96 bg-gradient-to-b from-sky-200 to-green-200 rounded-lg p-4">
        
        {/* Opponent's Pokemon section */}
        <div className="absolute top-4 right-4 w-64">
          <div className="bg-white rounded-lg p-2 mb-2">
            <div className="flex justify-between items-center">
              <div>
                <p className="font-bold">{battleState.opponent.name}</p>
                <p className="text-sm">N. {battleState.opponent.level}</p>
              </div>
              <div>
                <p className="text-sm">
                  {battleState.opponent.currentHP}/{battleState.opponent.maxHP} PV
                </p>
                {/* HP Bar */}
                <div className="w-32 h-2 bg-gray-200 rounded-full">
                  <div 
                    className="h-full bg-green-500 rounded-full"
                    style={{
                      width: `${(battleState.opponent.currentHP / battleState.opponent.maxHP) * 100}%`
                    }}
                  />
                </div>
              </div>
            </div>
          </div>
          <img 
            src={battleState.opponent.sprite} 
            alt="Opponent Pokemon"
            className="w-32 h-32 object-contain"
          />
        </div>

        {/* Player's Pokemon section */}
        <div className="absolute bottom-4 left-4 w-64">
          <img 
            src={battleState.player.sprite} 
            alt="Player Pokemon"
            className="w-32 h-32 object-contain mb-2"
          />
          <div className="bg-white rounded-lg p-2">
            <div className="flex justify-between items-center">
              <div>
                <p className="font-bold">{battleState.player.name}</p>
                <p className="text-sm">N. {battleState.player.level}</p>
              </div>
              <div>
                <p className="text-sm">
                  {battleState.player.currentHP}/{battleState.player.maxHP} PV
                </p>
                {/* HP Bar */}
                <div className="w-32 h-2 bg-gray-200 rounded-full">
                  <div 
                    className="h-full bg-green-500 rounded-full"
                    style={{
                      width: `${(battleState.player.currentHP / battleState.player.maxHP) * 100}%`
                    }}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Battle menu */}
        <div className="absolute bottom-0 left-0 right-0 bg-white rounded-t-lg p-4">
          <div className="grid grid-cols-2 gap-4">
            <button className="bg-gray-100 hover:bg-gray-200 p-2 rounded text-left">
              ATTAQUE
            </button>
            <button className="bg-gray-100 hover:bg-gray-200 p-2 rounded text-left">
              SAC
            </button>
            <button className="bg-gray-100 hover:bg-gray-200 p-2 rounded text-left">
              POKEMON
            </button>
            <button className="bg-gray-100 hover:bg-gray-200 p-2 rounded text-left">
              FUITE
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};

export default PokemonBattleScreen;