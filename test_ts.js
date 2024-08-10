"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var dex_1 = require("@pkmn/dex");
var data_1 = require("@pkmn/data");
var adaptable_1 = require("@smogon/calc/adaptable");
var gens = new data_1.Generations(dex_1.Dex);
var gen = gens.get(1);
var result = (0, adaptable_1.calculate)(gen, new adaptable_1.Pokemon(gen, 'Gengar'), new adaptable_1.Pokemon(gen, 'Vulpix'), new adaptable_1.Move(gen, 'Surf'), new adaptable_1.Field({ defenderSide: { isLightScreen: true } }));
