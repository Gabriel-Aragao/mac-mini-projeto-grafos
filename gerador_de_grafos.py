import pygame
import sys
import math
import json

pygame.init()

LARGURA, ALTURA = 1000, 700
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Gerador de Grafos")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 120, 0)

RAIO_NO = 20
LARGURA_ARESTA = 5

FONTE = pygame.font.Font(None, 28)

nos = []
arestas = []

no_selecionado = None




def gerar_id_no(indice):
    return chr(ord('a') + indice)

def salvar_grafo_em_json():
    grafo_para_salvar = {}

    for i in range(len(nos)):
        pos = nos[i]
        node_id = gerar_id_no(i)
        grafo_para_salvar[node_id] = {
            "posicao": pos,
            "arestas": []
        }

    for no1, no2 in arestas:
        id1 = gerar_id_no(no1)
        id2 = gerar_id_no(no2)
        
        pos1 = nos[no1]
        pos2 = nos[no2]
        
        distancia = math.dist(pos1, pos2)

        grafo_para_salvar[id1]["arestas"].append({
            "no": id2,
            "custo": round(distancia, 2)
        })
        
        grafo_para_salvar[id2]["arestas"].append({
            "no": id1,
            "custo": round(distancia, 2)
        })

    with open("grafo.json", "w") as write_file:
        json.dump(grafo_para_salvar, write_file, indent=4)

def desenhar_tela():
    TELA.fill(BRANCO)

    if arestas:
      for no1, no2 in arestas:
          pos_inicio = nos[no1]
          pos_fim = nos[no2]
          
          pygame.draw.line(TELA, PRETO, pos_inicio, pos_fim, LARGURA_ARESTA)

          distancia = math.dist(pos_inicio, pos_fim)
          ponto_medio = ( (pos_inicio[0] + pos_fim[0]) / 2, (pos_inicio[1] + pos_fim[1]) / 2 )
          
          texto_dist = FONTE.render(f"{distancia:.1f}", True, PRETO)
          
          rect_fundo = texto_dist.get_rect(center=ponto_medio)
          pygame.draw.rect(TELA, BRANCO, rect_fundo)
          
          TELA.blit(texto_dist, texto_dist.get_rect(center=ponto_medio))

    for i in range(len(nos)):
        pos = nos[i]
        cor = VERDE if i == no_selecionado else AZUL
        pygame.draw.circle(TELA, cor, pos, RAIO_NO)
        
        id_no = gerar_id_no(i)
        texto_no = FONTE.render(id_no, True, BRANCO)
        rect_texto = texto_no.get_rect(center=pos)
        TELA.blit(texto_no, rect_texto)
        
    instrucoes = "Para criar NÓS e ARESTAS use o botão esquerdo. Aperte [S] para salvar"

    texto_ajuda = FONTE.render(instrucoes, True, PRETO)
    TELA.blit(texto_ajuda, (10, 10))
        
    pygame.display.flip()

def main():
    global nos, arestas, no_selecionado
    
    rodando = True
    clock = pygame.time.Clock()

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    salvar_grafo_em_json()
                    pygame.image.save(TELA, "grafo.png")
                    rodando = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos_mouse = event.pos
                no_clicado = None

                for i in range(len(nos)):
                    pos_no = nos[i]
                    distancia = math.hypot(pos_mouse[0] - pos_no[0], pos_mouse[1] - pos_no[1])
                    if distancia <= RAIO_NO:
                        no_clicado = i
                        break
                
                if no_clicado is not None:
                    if no_selecionado is None:
                        no_selecionado = no_clicado
                    else:
                        if no_selecionado != no_clicado:
                            aresta = tuple(sorted((no_selecionado, no_clicado)))
                            if aresta not in arestas:
                                arestas.append(aresta)
                        no_selecionado = None
                else:
                    nos.append(pos_mouse)
                    no_selecionado = None

        desenhar_tela()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()