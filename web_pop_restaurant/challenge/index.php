<?php
//error_reporting(0);

require_once 'Helpers/CheckAuthentication.php';
require_once 'Helpers/ArrayHelpers.php';
require_once 'Models/IceCreamModel.php';
require_once 'Models/PizzaModel.php';
require_once 'Models/SpaghettiModel.php';
require_once 'Models/DatabaseModel.php';

use Helpers\ArrayHelpers;

isAuthenticated();
$username = $_SESSION['username'];
$id = $_SESSION['id'];
$db = new Database();
$orders = $db->getOrdersByUser($id);
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Order Food</title>
  <style>
    @import url("https://fonts.googleapis.com/css2?family=Silkscreen:wght@400;700&display=swap");

    * {
      padding: 0;
      margin: 0;
      box-sizing: border-box;
      font-family: "Silkscreen", sans-serif;
      color: white;
    }

    body, html {
      height: 100%;
      background-color: black;
    }

    .app {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      background-image: url('Static/Images/background.gif');
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
    }

    .order {
      width: 100%;
      max-width: 500px;
      background-color: rgba(0, 0, 0, 0.7);
      padding: 40px;
      border-radius: 20px;
      text-align: center;
      margin-bottom: 20px;
    }

    .order__desc {
      margin-bottom: 20px;
      font-size: 24px;
      text-transform: uppercase;
    }

    .order__buttons {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 20px;
      margin-top: 20px;
    }

    .order__button {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 10px 20px;
      background-color: #af5865;
      color: white;
      cursor: pointer;
      border: none;
      border-radius: 5px;
      text-transform: uppercase;
      text-align: center;
    }

    .order__button img {
      width: 100px; /* Adjust image size as needed */
      height: auto;
      margin-bottom: 10px;
      border-radius: 5px;
    }

    .order__group > input {
      display: none; /* Hide the input fields, as they are not needed for display */
    }

    .orders__list {
      margin-top: 20px;
      padding: 20px;
      background-color: rgba(255, 255, 255, 0.1);
      border-radius: 10px;
    }

    .order__item {
      display: flex;
      align-items: center;
      margin-bottom: 10px;
      font-size: 18px;
    }

    .order__item img {
      width: 24px; /* Icon size */
      height: 24px; /* Icon size */
      margin-right: 10px;
    }
  </style>
</head>
<body>
  <div class="app">
    <main>
      <section class="order">
        <div class="order__container">
          <div class="order__desc">Hello, <?php echo htmlentities($username); ?>! Place your food order</div>
          <div class="order__buttons">
            <form action="order.php" method="POST">
              <input type="hidden" name="data" value="<?php echo base64_encode(serialize(new Pizza())); ?>">
              <button type="submit" class="order__button">
                <img src="Static/Images/Pizza.gif" alt="Pizza">
                Order Pizza
              </button>
            </form>
            <form action="order.php" method="POST">
              <input type="hidden" name="data" value="<?php echo base64_encode(serialize(new IceCream())); ?>">
              <button type="submit" class="order__button">
                <img src="Static/Images/IceCream.gif" alt="Ice Cream">
                Order Ice Cream
              </button>
            </form>
            <form action="order.php" method="POST">
              <input type="hidden" name="data" value="<?php echo base64_encode(serialize(new Spaghetti())); ?>">
              <button type="submit" class="order__button">
                <img src="Static/Images/Spaghetti.gif" alt="Spaghetti">
                Order Spaghetti
              </button>
            </form>
          </div>
        </div>
      </section>

      <!-- New section for displaying orders -->
      <section class="order">
        <div class="order__container">
          <div class="order__desc">Your Orders</div>
          <div class="orders__list">
            <?php if (empty($orders)): ?>
              <p>You have no orders.</p>
            <?php else: ?>
              <?php foreach ($orders as $order): ?>
                <div class="order__item">
                  <img src="<?php echo "Static/Images/".$order['food_item'].".gif"; ?>" alt="<?php echo htmlspecialchars($order['food_item']); ?>">
                  Order ID: <?php echo htmlspecialchars($order['order_id']); ?> - Food Item: <?php echo htmlspecialchars($order['food_item']); ?>
                </div>
              <?php endforeach; ?>
            <?php endif; ?>
          </div>
        </div>
      </section>
    </main>
  </div>
</body>
</html>