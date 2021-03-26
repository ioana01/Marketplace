"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time

class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, group=None, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.ID = marketplace.register_producer()
        self.current_product_nr = 0

    def run(self):
        while 1:
            for _ in range(0, self.products[self.current_product_nr][1]):
                time.sleep(self.products[self.current_product_nr][2])

                while not self.marketplace.publish(self.ID, self.products[self.current_product_nr]):
                    time.sleep(self.republish_wait_time)
            if self.current_product_nr == len(self.products) - 1:
                self.current_product_nr = 0
            else:
                self.current_product_nr = self.current_product_nr + 1
