"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.current_producer_id = -1
        self.current_cart_id = -1
        self.consumer_shopping_list = []
        self.producer_items_list = []

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.current_producer_id = self.current_producer_id + 1
        self.producer_items_list.append([])

        return self.current_producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        if len(self.producer_items_list[producer_id]) == self.queue_size_per_producer:
            return False
            
        self.producer_items_list[producer_id].append(product)
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.current_cart_id = self.current_cart_id + 1
        self.consumer_shopping_list.append([])

        return self.current_cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        for i in range(0, len(self.producer_items_list)):
            for prod in self.producer_items_list[i]:
                if prod[0] == product:
                    self.consumer_shopping_list[cart_id].append((prod, i))
                    self.producer_items_list[i].remove(prod)
                    return True

        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        searched_list = self.consumer_shopping_list[cart_id]
        for (prod, producer_id) in searched_list:
            if prod[0] == product:
                self.producer_items_list[producer_id].append(prod)
                for product_search in self.producer_items_list[producer_id]:
                    if product_search[0] == product:
                        self.consumer_shopping_list[cart_id].remove((product_search, producer_id))
                        break
                break
                        
    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        return self.consumer_shopping_list[cart_id]
