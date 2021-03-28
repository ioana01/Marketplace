"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.cart_id = marketplace.new_cart()
        self.name = kwargs['name']

    def run(self):
        # The list of carts is iterated
        for i in range(0, len(self.carts)):
            # The list of products of the current cart is iterated
            for j in range(0, len(self.carts[i])):
                # Check the type of the operation
                if self.carts[i][j]['type'] == 'add':
                    # Call the add_to_cart method until the desired quantity is added
                    # If the product is not available, the consumer will wait
                    for _ in range(0, self.carts[i][j]['quantity']):
                        while not self.marketplace.add_to_cart(
                                self.cart_id, self.carts[i][j]['product']):
                            time.sleep(self.retry_wait_time)
                elif self.carts[i][j]['type'] == 'remove':
                    # Call the remove_from_cart method until the desired quantity is removed
                    for _ in range(0, self.carts[i][j]['quantity']):
                        self.marketplace.remove_from_cart(self.cart_id, self.carts[i][j]['product'])

        # Print the final order of the consumer
        product_list = self.marketplace.place_order(self.cart_id)
        for product, _ in product_list:
            print(self.name, "bought", product[0])
