using System.Collections;
using UnityEngine;

public class ScriptPrefabBomba : MonoBehaviour
{
    //Este script es de la bomba


    [SerializeField]private GameObject explosion;
    private SpriteRenderer bombaSprite;
    private Animator animator;
    private void Start()
    {
        //Obtiene el sprite de la bomba el animator e inicia una corutina, todo esto cuando el objeto sea instanciado
        bombaSprite = GetComponent<SpriteRenderer>();
        animator = GetComponent<Animator>();
        StartCoroutine(Explosion());
    }

    //Corutina de la explosion
  IEnumerator Explosion() 
    {
        //Espera 2 segundos hasta activar la animacion de la explosion luego espera para activar el objeto de la explosion el cual es el encargado de hacer daño y desactiva el sprite para despues destruir al objeto.
        yield return new WaitForSeconds(2f);
        
        animator.SetBool("kaboom",true);
        yield return new WaitForSeconds(0.6f);
        AudioManager.instance.PlaySfx("kaboom");
        explosion.SetActive(true);
        if (bombaSprite != null)
        {
            bombaSprite.enabled = false;
        }
        yield return new WaitForSeconds(0.5f);
        Destroy(this.gameObject);
    }
}
