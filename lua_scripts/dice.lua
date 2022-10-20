local dice_sum = 0
local count_dice_rolls = 0

function onObjectRandomize(object, player_color)
    if object.getGUID() == '322d66' or object.getGUID() == '9716db' or object.getGUID() == 'd1e994' then
        count_dice_rolls = count_dice_rolls + 1
    end
    if count_dice_rolls > 3 then
        dice_sum = dice_sum + object.getValue() end
            if count_dice_rolls == 6 then
                print(dice_sum)
                dice_sum = 0
                count_dice_rolls = 0
                print(player_color) end
    end

function onRotate(spin, flip, player_color, old_spin, old_flip)
    if object.getGUID() == '322d66' or object.getGUID() == '9716db' or object.getGUID() == 'd1e994' then
        dice_sum = 0
        count_dice_rolls = 0
        print('Значения сброшены')
    end
end