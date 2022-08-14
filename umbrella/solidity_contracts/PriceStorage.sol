// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "../interfaces/AggregatorV3Interface.sol";

contract PriceConsumer {
    // initialization of variables
    AggregatorV3Interface internal priceFeed;
    int[] public prices;
    uint internal latestPrice;

    /**
     * Network: Rinkeby
     * Aggregator: ETH/USD
     * Address: 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
     */
    constructor() {
        priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
    }


    function getLastPrice() public view returns (int) {
        // function to get latest price
        (
            /*uint80 roundID*/,
            int price,
            /*uint startedAt*/,
            /*uint timeStamp*/,
            /*uint80 answeredInRound*/
        ) = priceFeed.latestRoundData();
        return price;
    }

    function storePrice() public {
        // function to store a given price
        int _price = getLastPrice();
        prices.push(_price);
    }

    function getPriceFromStorage(uint i) public view returns (int){
        return prices[i];
    }

    function getPricesFromStorageLength() public view returns (uint) {
        return prices.length;
    }
}