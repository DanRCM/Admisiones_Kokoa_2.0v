using UnityEngine;
using System.Collections;
using System.Collections.Generic;


public class movement : MonoBehaviour
{
    [Header("Movimiento Fuerzas")]
    [SerializeField]private float velocity;
    [SerializeField] private float fuerzaSprint;
    [SerializeField] private float fuerzaSalto;
    private bool isJumping;

    //Al saltar en los juegos hay algo llamado coyoteTime es como un margen de error para poder saltar
    private float coyoteTime = 0.2f;
    private float coyoteTimeCounter;

    //El jumpBufferTime es otra cosa usada, en pocas palabras hace es que si se da al espacio momentos antes de tocar el suelo a lo que toque el suelo pueda saltar
    private float jumpBufferTime = 0.2f;
    private float jumpBufferCounter;

    //Variable para permitir el doble salto
    private bool canDoubleJump;

    [Header("Capa a detectar (suelo)")]
    [SerializeField] private LayerMask suelo;
    
    [Header("Fuerza de retroceso")]
    [SerializeField] private float fuerzaGolpe;
 
    [Header("Particulas, Correr y Saltar")]
    [SerializeField] ParticleSystem particulas;



    //El animator del jugador
    private Animator animator;

    //El collider del Jugador
    private BoxCollider2D boxCollider;

    //El componente encargado de la fisica del jugador
    public Rigidbody2D rb;

    //Esta variable es para cambiar la orientacion del personaje
    private bool mirandoDerecha = false;
   
  
    private void Start()
    {
        //Obtiene los diferentes elementos del jugador(El objeto de fisicas, el collider y el animator)      
        rb = GetComponent<Rigidbody2D>();
        boxCollider = GetComponent<BoxCollider2D>();    
        animator = GetComponent<Animator>();

    }

    // Esta funcion se ejecuta cada frame y ejecuta las dos funciones principales(por el momento) del jugador el cual son sus dos movimientos.
    void Update()
    {
        //Cada frame se ejecutan estas funciones de los diferentes movimientos del personaje

   

            MoverHorizontal();
            movimientoVertical();
            mejoraDobleSalto();

   
       

        //Esto es solo para poder moverme entre escenas al final no va a estar
        if (Input.GetKeyDown(KeyCode.Tab))
        {
            gameManager.instance.cargarEscena();

        }

      
    }


    //Funcion que detecta cuando el jugador esta en el suelo
    bool estaEnSuelo()
    {
        RaycastHit2D raycastHit = Physics2D.BoxCast(boxCollider.bounds.center, new Vector2(boxCollider.bounds.size.x, boxCollider.bounds.size.y), 0f, Vector2.down, 0.2f,suelo);
        return raycastHit.collider != null;
    }

    //Movimiento vertical(Salto)
    private void movimientoVertical()
    {
       
        //Si esta en el suelo el coyoteTimeCounter se actualiza al tiempo maximo permitido de lo contrario se le resta
        if (estaEnSuelo())
        {
            coyoteTimeCounter = coyoteTime;
            //Si esta en el suelo se reinicia la variable que permite el doble salto
            canDoubleJump = true;
        }
        else
        {
            
            coyoteTimeCounter -= Time.deltaTime;
            
        }

        //Si se presiona la tecla espacio el contador del jumpBUFFER se actualiza al tiempo maximo permitido de lo contrario se le resta
        if (Input.GetButtonDown("Jump"))
        {
            jumpBufferCounter = jumpBufferTime;

        }
        else
        {
            jumpBufferCounter -= Time.deltaTime;
        }

        //Si el contador del coyote time es  mayor a 0 el jumpbuffer igual y no esta saltando hace que salte, actualiza el jumpBuffer a 0 para que no pueda volver a saltar
        // incia las particulas y aparte inicia un cooldown al salto.

        if (coyoteTimeCounter > 0f && jumpBufferCounter > 0f && !isJumping)
        {
            rb.linearVelocity = new Vector2(rb.linearVelocity.x, fuerzaSalto);
            particulas.Play();
            AudioManager.instance.PlaySfx("saltar");

            jumpBufferCounter = 0f;

            StartCoroutine(JumpCooldown());
        }

        //Esto es para que cuando la velocidad vaya disminuyendo si el boton deja de estar presionado.
        if (Input.GetButtonUp("Jump") && rb.linearVelocity.y > 0f)
        {
            rb.linearVelocity = new Vector2(rb.linearVelocity.x, rb.linearVelocity.y * 0.5f);

            coyoteTimeCounter = 0f;
        }
    }

    //Cooldown del salto
    private IEnumerator JumpCooldown()
    {
        isJumping = true;
        yield return new WaitForSeconds(0.4f);
        isJumping = false;
    }


    //Movimiento Horizontal
    private void MoverHorizontal()
    {
        //Input.GetAxis pasa de menos 1 hasta 1 dependiendo de cual tecla se use para moverse de manera horizontal derecha es igual a 1, izquierda menos 1
        float inputMovimiento = Input.GetAxis("Horizontal");

        //Esto pone la velocidad de caminata
        rb.linearVelocity = new Vector2 (velocity * inputMovimiento, rb.linearVelocityY);


       //Sprint si se presiona el shift y si esta movimiendo muestra las particulas y se mueve mas rapido
        if (Input.GetKey(KeyCode.LeftShift) && inputMovimiento != 0)
        {
            particulas.Play();
            rb.linearVelocity = new Vector2(fuerzaSprint * inputMovimiento, rb.linearVelocityY);
        }
 
        //Esto es apra mostrar las animaciones si alcanza cierta velocidad camina, si la rebasa corre y de los contrario es porque esta  quieto
        if (Mathf.Abs(rb.linearVelocityX) < 5f && Mathf.Abs(rb.linearVelocityX) > 0)
        {
            animator.SetBool("IsWalking", true);
            animator.SetBool("IsRunning", false);
        }
        else if (Mathf.Abs(rb.linearVelocityX) > 5f )
        {
            animator.SetBool("IsWalking", false);
            animator.SetBool("IsRunning", true);
        }
        else
        {
            animator.SetBool("IsRunning", false);
            animator.SetBool("IsWalking", false);
        }
        Orientacion(inputMovimiento);
    }


    //Cambia la orientacion del jugador
    private void Orientacion(float inputMovimiento)
    {
        if (mirandoDerecha == true && inputMovimiento>0 || mirandoDerecha == false && inputMovimiento<0)
        {
            mirandoDerecha = !mirandoDerecha;
            
            transform.localScale = new Vector2(-transform.localScale.x,transform.localScale.y);
        }
    }


    //Metodo daño del jugador, se accede desde otro script
    public void damage()
    {
         // Lo unico que hace es motrar una animacion y aplicar una fuerza a la direccion contraria de donde esta el objeto causante del daño
            Vector2 direccionGolpe;
            if (rb.linearVelocityX > 0)
            {
                direccionGolpe = new Vector2(-2, 3);
            }
            else
            {
                direccionGolpe = new Vector2(2, 3);
                direccionGolpe = new Vector2(2, 3);
            }
        AudioManager.instance.PlaySfx("dano");
        animator.SetTrigger("gotHit");
        rb.linearVelocity = new Vector2(0, 0);
        rb.AddForce(direccionGolpe * fuerzaGolpe);
      
    }

    //Mejora de doble salto
    private void mejoraDobleSalto()
    {
        //Si se salta tiene doble saltos disponibles y ademas no esta en el suelo podra saltar
        if (gameManager.instance.dobleSaltos > 0   && Input.GetButtonDown("Jump") && !estaEnSuelo())
        {  
            if (canDoubleJump){
                //Reinicio la velocidad en y le anado la velocidad que le corresponde.
                rb.linearVelocity = new Vector2(rb.linearVelocity.x, 0);
                AudioManager.instance.PlaySfx("saltar");
                rb.linearVelocity = new Vector2(rb.linearVelocity.x, fuerzaSalto);
                particulas.Play();

             

                //Actualizo la cantidad de doble saltos permitidos
                gameManager.instance.usarDobleSalto();

                canDoubleJump = false;

            }


        }

        //Si deja de presionar el boton caera mas rapido
        if (Input.GetButtonUp("Jump") && rb.linearVelocity.y > 0f)
        {
            rb.linearVelocity = new Vector2(rb.linearVelocity.x, rb.linearVelocity.y * 0.5f);

        }
    }





 }
    
  
