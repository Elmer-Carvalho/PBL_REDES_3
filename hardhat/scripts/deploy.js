const hre = require("hardhat");

async function main() {
  try {
    console.log("Iniciando deploy do contrato...");

    // Verificar saldo da conta
    const [deployer] = await hre.ethers.getSigners();
    const balance = await deployer.getBalance();
    console.log(`Conta de deploy: ${deployer.address}`);
    console.log(`Saldo da conta: ${hre.ethers.utils.formatEther(balance)} ETH`);

    if (balance.eq(0)) {
      throw new Error("Conta de deploy não possui saldo suficiente");
    }

    // Deploy do contrato
    const PostosAbastecimento = await hre.ethers.getContractFactory(
      "PostosAbastecimento"
    );
    console.log("Deployando contrato...");

    const postos = await PostosAbastecimento.deploy();
    await postos.deployed();

    console.log("Contrato deployado com sucesso!");
    console.log("Endereço do contrato:", postos.address);

    // Verificar se o contrato foi deployado corretamente
    const code = await hre.ethers.provider.getCode(postos.address);
    if (code === "0x") {
      throw new Error("Contrato não foi deployado corretamente");
    }

    console.log("Verificação do contrato concluída com sucesso!");
    return postos.address;
  } catch (error) {
    console.error("Erro durante o deploy:", error);
    process.exit(1);
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
