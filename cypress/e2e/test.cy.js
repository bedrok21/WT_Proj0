require(`@4tw/cypress-drag-drop`)
describe("Todo List App", () => {
  beforeEach(() => {
    cy.visit("http://localhost:8000");
  });

  it("Adds three tasks", () => {
    cy.get("#todo-input").type("Task 1");
    cy.get("#add-button").click();
    cy.get("#todo-input").type("Task 2");
    cy.get("#add-button").click();
    cy.get("#todo-input").type("Task 3");
    cy.get("#add-button").click();

    cy.get(".todo-item").should("have.length", 3);

    cy.get(".todo-item:eq(1) input[type='checkbox']").check();

    cy.get(".todo-item:eq(1)").should("have.class", "completed");

    cy.get(".todo-item").eq(0).find("input[type='checkbox']").check();

    cy.get(".todo-item").eq(0).should("have.class", "completed");

    cy.get(".todo-item").eq(1).find(".delete-button").click();

    cy.get(".todo-item").should("have.length", 2);

    cy.get(".todo-item").eq(0).should("contain", "Task 1");
    cy.get(".todo-item").eq(1).should("contain", "Task 3");
  });
});
