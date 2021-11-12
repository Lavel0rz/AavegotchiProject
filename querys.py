query = '''
{
  erc721Listings (orderBy:district,first:1000,where:{category:4,timePurchased_gt:0,cancelled:false}) {
 		category
    priceInWei
    size
    timePurchased
    district
    parcel {
 			  id
 			}
  }
}



'''
query2= '''
{
  erc721Listings (orderBy:tokenId,first:1000,where:{category:4,timePurchased:0,cancelled:false}) {
         id
    category
    priceInWei
    size
    timePurchased
    district
    coordinateX
    coordinateY
    parcel {
               id 
             }
  }
}



'''
query3 = '''
{
  erc721Listings (orderBy:tokenId,first:1000,skip:1000,where:{category:4,timePurchased:0,cancelled:false}) {
         id
    category
    priceInWei
    size
    timePurchased
    district
    coordinateX
    coordinateY
    parcel {
               id 
             }
  }
}

'''
query4 = '''
{
  erc721Listings (orderBy:tokenId,first:1000,where:{category:4,timePurchased:0,cancelled:false}) {
         id
    category
    priceInWei
    size
    timePurchased
    district
    coordinateX
    coordinateY
    parcel {
               id 
             }
  }
}

'''
query5 = '''
{
  erc721Listings (orderBy:tokenId,first:1000,skip:1000,where:{category:4,timePurchased:0,cancelled:false}) {
         id
    category
    priceInWei
    size
    timePurchased
    district
    coordinateX
    coordinateY
    parcel {
               id 
             }
  }
}

'''
query6 = '''
{
  erc721Listings (orderBy:tokenId,first:1000,skip:2000,where:{category:4,timePurchased:0,cancelled:false}) {
         id
    category
    priceInWei
    size
    timePurchased
    district
    coordinateX
    coordinateY
    parcel {
               id 
             }
  }
}

'''
query7 = '''
{
  erc721Listings (orderBy:tokenId,first:1000,skip:2000,where:{category:4,timePurchased:0,cancelled:false}) {
         id
    category
    priceInWei
    size
    timePurchased
    district
    coordinateX
    coordinateY
    parcel {
               id 
             }
  }
}

'''