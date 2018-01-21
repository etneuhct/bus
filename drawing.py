import pyglet

if __name__ == '__main__':
    app = pyglet.App
    game_area = None

    labels = [pyglet.text.Label("0"*8,
              font_name = "Times New Roman",
              font_size=18,
              color = (255, 0, 0, 255),
              x = app.width // 2,
              y = app.height // 2 - n,
              anchor_x = "center",
              anchor_y = "center") for n in range(0, 100, 18)]

    @app.event
    def on_draw():
        app.clear()
        [label.draw() for label in labels]
        pyglet.graphics.draw(4, pyglet.gl.GL_LINES,
            ("v2f", (0, 0, 0, app.height, app.width / 2, app.height, app.width / 2, 0))
        )

    pyglet.app.run()