import { Dex } from '@pkmn/dex';
import { Generations } from '@pkmn/data';
import { calculate, Pokemon, Move, Field } from '@smogon/calc/adaptable';

const gens = new Generations(Dex);

const gen = gens.get(1);
const result = calculate(
    gen,
    new Pokemon(gen, 'Gengar'),
    new Pokemon(gen, 'Vulpix'),
    new Move(gen, 'Surf'),
    new Field({ defenderSide: { isLightScreen: true } })
);