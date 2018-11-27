
in_feet = lambda inches : inches / 12.0

def main():
    print('\nEnter dimensions of the  tile in inches')
    tile_wd = int(input('Width : '))
    tile_ht = int(input('Height  : '))

    print ('\nTile : W X H =  {}" X {}"'.format(tile_wd, tile_ht))

    tile_area = tile_wd * tile_ht

    tile_price = int(input('\nEnter price per tile in (Rs) : '))

    print ('\nEnter dimensions of the Floor in feet')

    floor_wd = int(input('Room Width  : '))
    floor_ht = int(input('Room Height : '))
    floor_area = floor_wd * floor_ht

    print('\nThe area of the floor is : {0:1.2f} sq. foot'.format(floor_area))

    tile_wd_feet = in_feet(tile_wd)
    tile_ht_feet = in_feet(tile_ht)
        
    tile_area = tile_wd_feet * tile_ht_feet

    num_of_tiles = floor_area / tile_area

    total_cost = num_of_tiles * tile_price

    print('\nThe total cost of floor is : {0:1.2f} Rs.'.format(total_cost))

if __name__ == "__main__":
    main()
