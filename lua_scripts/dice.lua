print('importing sqlite3...')
sqlite3 = require "luasql.sqlite3"

print('create enviroment')
local env  = sqlite3.sqlite3()

print('create connection to db')
local conn = env:connect([['C:\Users\User\PycharmProjects\infobot\lua_scripts\lua_dice.db']])
print(env,conn)

print('initialize local variables')
local dice_sum = 0
local count_dice_rolls = 0


function onObjectRandomize(object, player_color)
    if object.getGUID() == '322d66' or object.getGUID() == '9716db' or object.getGUID() == 'd1e994' then
        count_dice_rolls = count_dice_rolls + 1
    end
    if count_dice_rolls > 3 then
        dice_sum = dice_sum + object.getValue() end
            if count_dice_rolls == 6 then
                print('Игрок ', player_color, ' роллит: ', dice_sum)
                dice_sum = 0
                count_dice_rolls = 0 end
    end

function onScriptingButtonUp(index, player_color)
    print('a')
        if index==0 and player_color then
            dice_sum = 0
            count_dice_rolls = 0
            print('Значения сброшены')end
    end