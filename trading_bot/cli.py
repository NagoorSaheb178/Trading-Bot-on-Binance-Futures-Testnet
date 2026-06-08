import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
from typing import Optional

from bot.orders import OrderManager
from bot.validators import validate_symbol, validate_quantity, validate_price, validate_stop_price

app = typer.Typer(help="Binance Futures Testnet Trading Bot CLI")
console = Console()

@app.command()
def place_order(
    symbol: str = typer.Option(..., "--symbol", "-s", prompt="Trading Symbol (e.g., BTCUSDT)", help="The trading pair symbol."),
    side: str = typer.Option(..., "--side", "-d", prompt="Order Side (BUY/SELL)", help="BUY or SELL."),
    order_type: str = typer.Option(..., "--order-type", "-t", prompt="Order Type (MARKET/LIMIT/STOP_LIMIT)", help="Type of the order."),
    quantity: float = typer.Option(..., "--quantity", "-q", prompt="Quantity", help="Amount to trade."),
    price: Optional[float] = typer.Option(None, "--price", "-p", help="Price (Required for LIMIT and STOP_LIMIT orders)."),
    stop_price: Optional[float] = typer.Option(None, "--stop-price", "-sp", help="Stop Price (Required for STOP_LIMIT orders).")
):
    """
    Place a new order on Binance Futures Testnet.
    """
    try:
        # Step 1: Validate input
        symbol = validate_symbol(symbol)
        
        side = side.upper()
        if side not in ["BUY", "SELL"]:
            raise ValueError("Side must be BUY or SELL.")
            
        order_type = order_type.upper()
        if order_type not in ["MARKET", "LIMIT", "STOP_LIMIT"]:
            raise ValueError("Order type must be MARKET, LIMIT, or STOP_LIMIT.")
            
        quantity = validate_quantity(quantity)
        
        # If interactive prompt didn't get price for limit order, prompt here.
        if order_type in ["LIMIT", "STOP_LIMIT"] and price is None:
            price = typer.prompt("Price", type=float)
        price = validate_price(price, order_type)

        if order_type == "STOP_LIMIT" and stop_price is None:
            stop_price = typer.prompt("Stop Price", type=float)
        stop_price = validate_stop_price(stop_price, order_type)

    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/bold red] {e}")
        raise typer.Exit(code=1)

    # Step 2: Display Summary
    summary_table = Table(title="Order Request Summary", show_header=True, header_style="bold magenta")
    summary_table.add_column("Parameter", style="cyan")
    summary_table.add_column("Value", style="green")
    
    summary_table.add_row("Symbol", symbol)
    summary_table.add_row("Side", side)
    summary_table.add_row("Order Type", order_type)
    summary_table.add_row("Quantity", str(quantity))
    if price is not None:
        summary_table.add_row("Price", str(price))
    if stop_price is not None:
        summary_table.add_row("Stop Price", str(stop_price))

    console.print(summary_table)

    confirm = typer.confirm("Do you want to proceed with this order?")
    if not confirm:
        console.print("[yellow]Order cancelled by user.[/yellow]")
        raise typer.Exit()

    # Step 3: Execute Order
    with console.status("[bold green]Executing order on Binance Testnet...[/bold green]"):
        try:
            manager = OrderManager()
            result = manager.place_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price,
                stop_price=stop_price
            )
        except Exception as e:
            console.print(f"[bold red]Initialization Error:[/bold red] {str(e)}")
            raise typer.Exit(code=1)

    # Step 4: Handle Response
    if result["success"]:
        data = result["data"]
        
        response_table = Table(title="Order Response Details", show_header=True, header_style="bold green")
        response_table.add_column("Field", style="cyan")
        response_table.add_column("Value", style="white")

        # Extract relevant info
        response_table.add_row("Order ID", str(data.get('orderId', 'N/A')))
        response_table.add_row("Status", str(data.get('status', 'N/A')))
        response_table.add_row("Executed Qty", str(data.get('executedQty', 'N/A')))
        response_table.add_row("Avg Price", str(data.get('avgPrice', 'N/A')))

        console.print(response_table)
        console.print(Panel("[bold green]Order placed successfully![/bold green]", border_style="green"))
    else:
        console.print(Panel(f"[bold red]Order failed![/bold red]\n{result['error']}", border_style="red"))
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
