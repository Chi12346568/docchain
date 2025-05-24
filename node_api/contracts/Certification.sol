// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract CRTF is ERC721URIStorage, Ownable {
    uint256 public nextTokenId;

    event CertificateMinted(address indexed recipient, uint256 indexed tokenId, string tokenURI);

    constructor(string memory name_, string memory symbol_, address initialOwner)
        ERC721(name_, symbol_)
    {
        // Définir explicitement le propriétaire du contrat
        transferOwnership(initialOwner);
    }

    function mintCertificate(address recipient, string memory tokenURI) public onlyOwner {
        require(recipient != address(0), "Invalid address");

        uint256 tokenId = nextTokenId;
        _mint(recipient, tokenId);
        _setTokenURI(tokenId, tokenURI);

        emit CertificateMinted(recipient, tokenId, tokenURI);

        nextTokenId++;
    }

    function getCertificateURI(uint256 tokenId) public view returns (string memory) {
        require(_exists(tokenId), "Token does not exist");
        return tokenURI(tokenId);
    }
}
