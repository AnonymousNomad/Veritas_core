import click
from .logger import logger
from .config import load_config
from .src.brain.brain_interface import VitalisBrain
from .src.core.vitalis_engine import VitalisEngine
from .src.extensions.evolutionary_lora import EvolutionaryLoRA

_cfg = load_config()

@click.group()
def cli():
    """Vitalis - Sovereign Free-Energy Synthetic Intelligence"""
    pass

@cli.command()
def run():
    """Start the interactive console (heartbeat + brain)."""
    engine = VitalisEngine()
    engine.wake_up()

    brain = VitalisBrain()
    from .src.core.heartbeat_loop import HeartbeatLoop
    hb = HeartbeatLoop(brain, interval=1.0)
    hb.start()

    click.echo("Brain ready - type 'exit' to quit.")
    while True:
        user = click.prompt("You", type=str)
        if user.lower() == "exit":
            logger.info("User requested shutdown")
            break
        resp = brain.generate_response(user, "SYSTEM: USER_INPUT")
        click.echo(f"Vitalis: {resp}")

    hb.stop()
    hb.join()

@cli.command()
@click.option("-g", "--generations", default=3, help="Number of LoRA evolution steps")
def evolve(generations: int):
    """Run the Evolutionary LoRA optimizer."""
    brain = VitalisBrain()
    evo = EvolutionaryLoRA(brain)
    for i in range(generations):
        logger.info(f"LoRA evolution step {i + 1}/{generations}")
        evo.run_generation()
    click.echo("Evolution finished. Sovereign weights updated locally.")

@cli.command()
def status():
    """Print system status."""
    click.echo("STATUS: VITALIS CORE ONLINE. Local Execution Confirmed.")

if __name__ == "__main__":
    cli()
