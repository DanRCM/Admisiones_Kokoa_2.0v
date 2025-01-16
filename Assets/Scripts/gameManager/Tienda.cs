using UnityEngine;
using TMPro;
using UnityEngine.UI;
public class Tienda : MonoBehaviour
{
    public Button dash;
    public Button doubleJump;
    public TextMeshProUGUI cantDobleSaltos;
    public TextMeshProUGUI dashText;
    public TextMeshProUGUI monedas;

    void Start()
    {
        monedas.text = gameManager.instance.monedasUsables.ToString();
        dashText.text = "No Comprado";
        cantDobleSaltos.text = gameManager.instance.dobleSaltos.ToString();
    }

    public void ComprarDash()
    {
        if (gameManager.instance.getMonedasUsables() >= 100 && !gameManager.instance.getDash())
        {
            gameManager.instance.changeDash();
            dashText.text = "Comprado";
            gameManager.instance.changeMonedasUsables(100);
            monedas.text = gameManager.instance.getMonedasUsables().ToString();
        }
    }

    public void comprarSaltos()
    {
        if (gameManager.instance.getMonedasUsables() >= 200)
        {
            gameManager.instance.changeDoublejump();
            cantDobleSaltos.text = gameManager.instance.getDoublejump().ToString();
            gameManager.instance.changeMonedasUsables(200);
            monedas.text = gameManager.instance.getMonedasUsables().ToString();
        }
    }
}
